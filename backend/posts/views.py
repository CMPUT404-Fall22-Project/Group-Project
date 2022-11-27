from django.shortcuts import get_object_or_404
from utils.model_utils import get_host, generate_random_string
from utils.requests import paginate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
from authors.models import Author
from .models import ContentType, Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from authors.serializers import AuthorSerializer
from inbox.views import add_data_to_inboxes_of_author_and_followers
import base64

post_example_filled = {
    "type": "post",
    "title": "A post title about a post about web dev",
    "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
    "origin": "http://whereitcamefrom.com/posts/zzzzz",
    "description": "This post discusses stuff -- brief",
    "contentType": "text/plain",
    "content": "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge",
    "author": {
        "type": "author",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Lara Croft",
        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "categories": ["web", "tutorial"],
    "count": 1023,
    "comments": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
    "commentsSrc": {
        "type": "comments",
        "page": 1,
        "size": 5,
        "post": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
        "comments": [
            {
                "type": "comment",
                "author": {
                    "type": "author",
                    "id": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                    "url": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                    "host": "http://127.0.0.1:5454/",
                    "displayName": "Greg Johnson",
                    "github": "http://github.com/gjohnson",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "comment": "Sick Olde English",
                "contentType": "text/markdown",
                "published": "2015-03-09T13:07:04+00:00",
                "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
            }
        ]
    },
    "published": "2015-03-09T13:07:04+00:00",
    "visibility": "PUBLIC",
    "unlisted": False
}

post_example_filled_img = post_example_filled.copy()
post_example_filled_img["contentType"] = "image/png;base64"
post_example_filled_img["content"] = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAA0UUlEQVR4nO29eZxU13Xv+137nFNDV1d308wzCBCDEMIMQjMgWbImNFhCicc4sfOuE/vj5zge4sQvEontl6cktu/LvXFy7evkxc6NLexcKRosWQPCkjUyygJJSGgCMwrooeZzzl7vj11V3UAD3U01oNi/j4puVVWfs89ea6+19pq28C6DKgIrDY/vE1m+Njrq85dvyJKTKYidgcpMjE4m1skIoxFpQ8kipFGSqngAIsQIZZQiQjeqHSh78eQtrH0L37yCmtfp4E1Zfk/HUfdcs9Rn2SiF1VYEPQXT0DDI6R5Af1AnOiCyOj7s/U3XTUfNIlTOx+p8RKcjZhQJSeAZ94RWwdZ+Vn9HqZNKqv8YwEj1Vf1dgVihEofAfuBV0I2IPIcnG5j3H9t6E111ped+e3cwwxnNAKq3G9gqhxF9441toBdj9RpgKTCL5sDHCEQWQguhoqoW1BFAEQRQcaSWvp9btUowqf7WQ0AREYNvIGHAN2AVzYWxwEvAz8E8SBA9KfPuP1S/3pqlPsuWWZFVtuGT0yCckQygd630WDlHaxOnm6/MQPoKYm5FuIKkGYdvoGKhHKNWYxFRRQUVg1D9r4FjgipTqBVEVVXEiEfSc0wRKlTi3QiPovITOjoekeVrc1Bl5NVbRW7rYeQzBWcUAzjx2SM6ddPNcxH7UazeStKbiidQjNEwtiJiVdW4xXl6nsMxhWptLBJ4hrTnVEY5ehPkx6j9gSy4b3PvZ+wt0U43zggGcCu+F+FfuOkaYvsHwDVkfJ9ijFZqRMc7XQQ/EZziUAuIJBwzaC60YuQBVL4t77nngfp371rpnQkS4bROpNPxUBf1m25+P8Z+Dk8uxgjkI4BIUSOIOZ1jHSgUrDhz0yfjO+Mz1KewfFMW3PNjOPr5TwdOj+isWvU1Uagbb7wW4U9JmouxihYiCygiptG6/FSjqiacVGjyDUYgjJ8m5mvynv+4H45WfacSp3xye4s+3XjjfET/ksBcD4IWQgsgMrjVrqpOAFchRpABPqG1h28PjWncFLmdCSpNgdsqRvYeyuEdcv4Dm+D0qIVTxgC9V70+dGWGUamv4Jk/ImGS2n1yhAdQq0jSh5TXQ8BCiEYW6QcRVRURgabA7f8BIosWwn79/YDG6hgByQaGii0T6bfo7PyqLF+bO9XS4JQwgOrtpq7n111/FQnzt6T8uXSHtS2cd1LXt4pkE7y9o4vn1v+KfK7IqNGtXLx4PC3NSbR4fCKqKuJ7WCM8vWEXr7/+Dr7vMWf2aM6bOwoKIVW/QEOhqrEY8cgGUIy3EvE5WXjPQ+6znjkbSgw5A+iapb4sXxvpA1cnGZv4Gr75YwQoxpFy8ha9jRWTTfCzx9/g+//rBeI4xhiII2gf3sRnPrWEmZPajskEqoAndEeWb337ObZu2YcfuPfjGJYtncrvf+Q8pBRhBqpP+gHnvCAm5fkIENpv0dH5ZVm+tlSbu4bftBeGlAFqe1599vrzSHrfJeMt0s6KRfsn7rWXLu5roNYqJh3wyhuHuOPrj9OSBd8X1Drd3Z2ztLU18bU/v5xmzzhJceQ9rCLZJP/vPzzHk0/tYNRI4+wAQAT27FU++qG53HjdTGxnGeMNzZSpqkVAWhOGQrSekv24LLlv81D7DYZka6WKOBG2OtZ1N36QtHmShFlERxgJYk5G1x95IzzDT+7ZSiIAzxOiSImtEkaW5mZh3/4CGzfthrSPWj3izxVJeuzZ1cXmF35F+zAhDC1xrPXXiOHCTx/axqEDRSTh9TBlgyEibqvbEUYE3kLS3pP63IoPi6yOVW83ejTvNgQNZwBHeFRkldUNN/w/ZMy/EtGs+TBG8AcygSLVVx+f2VgxLUme3/ArXty6j0xGiGM9zOpXBSPC7ncKPYEdDv8cz7C/o0QYWkSOZBDwPOjurnDPT19BMgEaD7FaFnzNhzGRNpP1v68bV9wpssqKoDW/QSPR0AvqXSs9kVVWn1qZ1o03rqYl+KLmw9hGVmuGXiPUqCqIJ5RKMT/89xdJpcDans8O/64ycli6GgE8HCJAbBneksQPpH6N3ohjJZsV1qx9g+2vHsA0J+oqYqggIp7GqpoPY7KJL+iGG36iD12ZEVll9a6VJ2UwH4mGMUBtD6tPrxhNU+URmr1bOVSOBPFMg60njS3SkuLH92xl964cqaSgR1BeRAhDZdiwJAvmjYE+jEARQcsxY8e3MGvmKIrFvvf9ThJZ/vl/bSYCOFqYNBwiiCAehyoRWf/9jE4/rI+sGC23rY4byQQNYQDVKvF/ce1kmmQNKe8iOioRIn4jrt8bNraY1hSbN+/mpz97ldZWJ/qPhDGQy8FVl8+gdXgTNoz7lD4KiFVuvGbWMYlqrdLUJLy2/SA/ueclTFsaG50i763g01GJSPsXMkIe1bU3TmwkE5w0AzixvzrWJ647i4z/KAlvNt1DQ3y1ikn5vHOoyD9+bz3p1NEiH9zKLpeVMWMzXHX5WWiugnh9P6oxguZDZs4awZLFE+nuVrw+LP04Vtpahf+4/2U2rN+F15YiPmVMID5dYUTCO4dWXaNPXHdWo5jgpBigLvbXXT+JFu9hEt40ctHQEF8VPKFiDH/37WfJdRdJJI4W/eBWf6EAK2+aS7opcN7A413cgBYjbrvpHNJpn+gYO29VpSkN3/7u8+zc1Y3XnMAOtVFYg+CTjyIS3jRa/If0masnNIIJBu96VYwT+1eOIjAPkvDOIh9FCA0jvlZftkpkaU7w9995ntdeO0A227fo9zyhq1tZtGgsF10wAdtdOuHe3dkCEaPGNHPzjXPo6lZ8v2+nke8LUVjhb//r0xzKVzApH9vHOIYEdSYw00klHtRfXDlKblsdqw6ejoMMuiDccTv61Mo06fQ9JP3ZbuU3jvjgtn/OeSNIS4r/8b0NPPvcTtra3H7/qO9XDb+mpgQf/e35aCly/v1+wHgG21Xi6vdO55w5I+nu1j4NQmuVdFo4cLCbO7/xC7pCi0mfYibIRRFp/xzS6Xv0qZVp7ridwfoJBswACsLjSz1ZtcqSKH2frH+B0/mNJT5UPX2egeYE3/7OOh57/A3aj0F8AM8IuRx89IPzGTmyCS33nwEARMGEMZ/4nQUkUgFx3Pe2NY6VbEbYubODr9/5BAeLESYTnEKbAGcTNPsXkCh/X1atsjy+1NNBeHYHLgHWLPVk+dpIn7/uTtoSt9AZhkOh8+PIYlI+RV/4m797hieefJP2YUJ0jJXm+8KBQ5arrpzGJRdPIu4sOeYZAMQIthQzdnQzH//owmNKAYAoVlqywu5dHfzl19fy9r78KTYM8emqhLQFt+jz190py9dGrFk6YHtgQBxT9+0/f91vk038G/koQhu78lVBrdvq7dyT479/+zl27DhEa+txVr4ndHcrZ88YyZc/fwmmFGJ08KkkNraYYWl+uPpF/vc9LzNi+PHvXSwqfpDg9z++iPMXjYeOIlYbm0twTAgRGd+no/xBueCBfxto7KDfI6yFJ3XjinPwzLMaa5pIG5qQaWOLCTxoTvDk0zv4l+9vpFKpkGk69sr3PKFQUNrbs/z5ny6lLTBo2L8cgOOOxTpX89/943M89dQO2tuPzQTGuM+KRbjuutncdtMsPKvYfIj4Zkgjbqoovqh4UqQcXSCL739xIKHkfo1NFWH1SsP8bp9c8Awpf77mw5OO49dgq1E6aUnS0VXm31Zv4Ykn3qA5A54vx3S91lZfOp3iK19eyrj2NLYQNSRipwoYiJI+f/2tp9iyZe8xjU/oiVt0dMDZM0fw0Q/NZ9rUNuguYyM7YHU0sLFqLJnAoxRtojm8gE3ZqHeS7fHQTwaoh3W/SXvys87Ld/Kiv074TAKANc/s4N//9xYOHijQ2uoIf6zgkecJpaKSSKb4ky9cypSxWWy+3NCJVquIbyh6hju/+Qu2vbyftmHHZgJwtkgupxjjcdVVZ3PD1dPJZBKQq2Bji3hDJBGUiLaET0fpm7L4/s/1VxWccCx1Z8/6FZeT9B7VchSLDn7lu7w9xRjj0q8ENr24j3seeJlXXn6HpiZIJPre49fg+0I+p2Syab7wuUsc8XONJX59vFaRwFAUwzf+7mm2bNnLsBMwgTHOQdXVBaNHN3PtNWezdMlEEmkf8iE2ctuLRtsIKhpL0vcohFfK+fc/0p8cw+OOwO0tbxfWr0+BbNSkN4NSpIOJ59dXe8KDVEBUjti4ZS8PP/Y6W1/ai2+gKXP8VQ+O+J2dypixrXz+sxcyZlgam68MrYitSoIw4fH331nH0087m+BEY/U855IuFmHCxBauWD6NixaPJ9uSrFY1RdhYEa8xhpSqWlKeSMW+jt96HvOmFWGVHk8VnIABqqL/uev+imGpLw1W9KtVpDkBCrv25Fj3wm6efmYHb+/owPegqckN5XhhVqlm6B48qMybN4ZPf3IxLQkPW2yMzu/XMxiB5gQ/uGsL99//Mi1ZMF7/xl0qKaUSjBiRZvHCCSxZNJ5pE1vxUj7kKo3LOaypgoPlO2XJfV86kSo45i31rpUet622PH/dOSS8DRqrwTLgPH1VRTIJnnh2J2sef4MdOw+Sz8ckk5BKuUsdawIFNy++J1RCJV+A971vJh9ZOQdTibGhPTVbrV7PgoK0pVj75Nv8yw82EoUhzc3HNw7VpcBhDIQVpVCEIIAxY1pZvHACK66aTkIVYnvSCRMKisGKb2Jiu4D33LuVu1aaY6mC465mAVWVvyHpB3RXYhmIW42ebN277n6Ju378Es0ZSCahrc0lX5wosUKMYAQ6u5SW1jSf+b35XLB4PHSWUE7RPrv3eKrpSfZQkaUXTWTq5Fa+808beO3VA7S2uvEcabvUVISqEsduV9Pa6p59//5OfnhXJ9teO8Aff/oCglou4smMEURjhSYvQVf8NwLXHG+W+y6Trht+172PVPCgFqNYGJjhp6pIymf7W538+dfX0Jp1iqg/2TQiPVZ+sQTnL5nEh397LiPa0sSdJTz/9FeJ2chimgIiEf79/m088NOXsXFMc7Nj7r6ilEdCRAgCYc8ey8c+Mo/rrp7RsMRTRWNp8j2KerUsvOehYxmEfUuAlXNU71rpERe/OugBWJDAZ+MLu+v67VgBk5qor+nLKFI6u5RxY7N8/P3ncNH546EQYrvKeL6pitTBjqwxML7BliJ8EW57/2wWvWcMP1y9hRdf3EMq5dTbiRhBVYkiZ/xufmEX1105vbHPpUBs/1L19oc5RhLTUUvJGQ2rLGcVbqAlWKSFga/+3iMo9ycgI4LnCXEMHR2K5ye59ZZz+Or/tZyLFo5DO8poZOsr43QTvwZjelTCWWOz/OnnLuIPPrmEESNbOdShVCouueS4qkrBiBKGMcTxgIJXx4MgnhaimKy/mPXrbxBZZXu6l/TgaAlwxxzV2zGo+bLGDD4ZWQCrTJk8jCh2+/7e+rG22lWVctlZyO3tKa64fCpXLZtK+4g0dFew3ZVTYuWfDIxn0JLLIrl0yXiWzB/D2md28uhj29mxowPfh3TaPe+RUsHzhUq3Mm5cKyQCbPHE+Qv9hoBaVFS+rMo93DHnKClw2J3q2751119F2n9IC7EVGWTOQPVnxTf85Z0/Z/v2QwwbJrVyWcIQSiU3gokTWrn4wslcumQire1pKFSwlXjovGZDCBurI2AmQVSJeW7zbtY+8SavbNtHpaKkkpBIOP0vAoWiIuLxF1+5nIkjM2hlYCHsE0EVK2nPkI+vkCX3PnakLXCEBKhyiOpn8YTqBmZQN3Z/rSSBz37qAv7hf25g27a9LkomMHx4E0sWj+L8hRM4Z+Zw/GTgCN9RRIwZUsfOUKK2em1XGd8IFy0az0WLxvP6Wx08t2EXL/xyN7t3d1EJFSMwYkSW3/ud+Uwcm0XzlYYXooIqvgET/RHwGCsPlwLS87VqtO+ZG+eQ1M0aqzf4gGqv21t13j/f8OrrB3nnnTytrWmmTGylqSXp9r7FyPnJjWmYfq+VeYuh3yvKWq0GdRpHhLoHNOVD0icuRry9q5O9e3M0NSWYNb2dRNIfkirkGhRUPImxZp4svPul3tHCHgnw+OMGsAT2d2lO+NJZiTiBn6A/ECNoGCNhzIyp7cyYMcIRvRxjO8v1GvyGrfgqf5tsEjyBUnTizKDqLsU0BRBZbCVumI+hdh0tR2gxxPMMUye0MnXKMCdgSxG2EA6pT0Mgpjnw6aj8HvCFOq2prvBqabzquuubsLxC0pugobXS4Mqh3j6Amg5sJLS6P5SUz8Nr32Tnzk4uu2QK0ya1HrtEvFodrEZ4+fVDDG9PMWpkMzY3dManak8MQczQNzxSsBIYQ2jfBp0ti+4rVHfSWl3hKw2sjrFcQXMwQfOhbVgBZy8MJZdbW03faknynX/awEM/e51EAE8+u4OvfmU5Y9vTLlGk1xAUQKAM/NdvP8umzXtoagr4xMcWcOGFk4gPFDBDkNAxFMx/3PuB0UpsJRNMohBdDtyHrjTI6tgReXX1m0Z+Sz1RETljGxv2BRtZTMIjTgf8w3fW8dhjrzN6lDB8uKFYCHn99QOQ9I9yyqhVpCngxa37WL9hD8OHCYaQv//H53js8Tfwhjch2j/v5ZkOEbHqiSL6W0Cd5r4T/6tjfebqFtArpRhLtRXbGY+agWWGpdizv8A/fncdr7y8vx6vF1ESCWHkyGbXRbTPiyjJhEc65UwTz4eMp3z3e+vY+atuPnDLHAIBW7XQG2kgnkqo4kkxFpSr9JmrW+SC1V2qiM/jSz1YG+EnLqXJGzVU4r+RcBa+YpoS4AuPPfEWd931SwqFMm1tPWXiUQStrUkmjGmGMD66ONQIVGKmTGglm01QLlfwDCDQ2iI8+OArbNu2nw994Dxmzxzu3NHl6F3JCCKIhrGVTDCKklwM/JTHl/YyvTW+Rv0zV/xrVRRrtSuIaU3x8psd/N/feIrvfncdcVymubknGufqA2HKpHaaWlJ9locJoJEl25ZiyqR2yuXqrqV6r7Y2YefOg/zVnY/znX/ayJ7OMqYtjSRcs4kTJYScaRARq74osV5be89n2dpqfVlpmVSsqKo5U7i7bi0rmMAg6QRY5eXXD/LgI9vZsGEHQi28rEe5mmML5507uhrX7tupoeqIPv/csWzYvOcw4yyOXRWQqvL449t5/vm3ufCCyVx+2RQmT2x1vaSLERrZ6nXcjQcze6o9LuKhMpZV1UjFCrDMNZtYFfsiqD5VnophJuW4IV4QRzSXQVPvu2dAenVxriXAKD3/1IgNbhIk8FzrN6DjUJFN63fxi2feYtu2/VgLmYwbbl/5g1GktGR95s8ZDaVjO1nECBQjFpw7mh9nA6IoPIwJagagq0sIeeTR13jiF68ze9ZoLlg0gXNnjaCtPe2mrRJDGKNxL8lQvdaRs1r/vLofE98gycB1IT9BV7NBQ0Qox2BkFus3T5VFbHezG+himgNfuyonn+pd7d7h8v5i/Ex1pxnFEKlrmdqrkE0E5xv2PPd3tVh/JWbvgQIvv3aQF17czcvb3uHQoTJBAE3pKuGt9hlu9YzQlVOWLB5D+6gM2ll21+5zTkArEe2jmjl37liefvZtWvooPK3ZFa2tgo0tv/zlbjZu2s2wYQlmTBvB7JmjOHtaO2NHZkg1J9z96mcU2Gqla5Xtpcp4nnGeFgvdHSW2bd1HS0uSGWe1QzFqTIpY72cFUauxtCR8usqLocYARs/HGTYnpdFqrVvysfLP313PG28eZMa0dmbPHMH4MS20tyRIphME1Y6pqhBZpVKKyOUrHOgssXdvjrd2dvL2jg527+kil4/xDKRSTtTX9PPxlG/tk8svmeqaPZ7Ap60iSBTz3sum8sxzbx9Xr9cYI5Nxe/lKucL6Dbt47vldJJPQ3p5h3JgsY0ZnGTMyw7BhaZqzSdKBh++58VciS64Y0tVZZNe+PG+/3cEbbx+io6NEGMLHPjKfq2t9DRosCUTEBSGQJcAP/eoMzCeyqJuKQV+8lgJ2z49+yaOPvcXwdnjiqW7WPvkWiQQ0pX2SyQSJhIfvGawqldBSKYeUSiGlsq0XZAYBJAJoa5W6fjxeqngNxrhKoVkzRzJnzkg0VzmhTjVG0ELIzLNHMPec0WzZspdM5vjJnrXPPA+amx0zWKt0dOTZvz/Phk17gFp2k8tmduNwzxFGVcGg7vNkElqyhmLJ8sij27jy4sl4Q6AGFBWJLIjMB/D1matbEGYQWhqSaiHCgYMFMhlIJg1+oPXJCcOIcjmqErSnmsYY92rO9Jggal1fgP4Q/YjbE8Vw4zUzEVUs/ZOkCkhsef/1s3lxy75+36+38QYQBFIN9x7+ufYycGoEr9lErh7SfadShlEjs5iEh+aP3rqePEQcrZmuT96QNYg/FRhFqJys718EKEdcfeUMjOdRCW2146bWWvpVJ0hIJt3PIBC8qtVhLfX+fPZ4cvgY8DxXM3DB+RM4d95obK7/QRZjBFuoMOPsESxfOpXOzr6bRJwIqlrfkcRx31tFrZoFse35jvGEcklpzqb48AfnI1HccBsAnFuYUAFG4+lUQ8B0El6g2leTtAFe3Ai2GDJjejt/+MnzKRSkWgVUXdX0rIbDXyd7Zyc5worS0pLkg7fNQwvRgE8YEGPQXIXfev85jB6doVg8dnl4I+F5QqWiqAR87v+8iHEjM2ipcelhR0LVWpImIMF0g2WGS/5oTOcz4xlsZ4klC8fx6U8toVAyhGHfjZcahZoqyRfg4x9byPC2FFoZ+ASKgMaWTNLnv3x8MWFksCefqn9c+L4rGkGSfOGPL+HsqW3Y3LF3LQ2C4hlQZhiUqY0WNcYz2EMlLlg4ni9+/lI8P0U+NziReiL0rhj67d86l0ULxmG7B59abYxg8xVmzRzBJ353AZ1dbus2FEzg+0JXl5JtaebP/uQyZp81jLhraGocj4J7nqkGkYlub95YNjC+wXaUOPfs4dz+Z8uYNGU4Bw+6HUijky0OHFBuuWUON1w7E9tZPOkJNJ7BdhRZeskUfvd3FtDZqVhLw6SY5zmGOnBQmTNnLHf82TKmjmnGdpfxTgXxFanSfJLouus3kPTfo+XIDsW5PDa2mFRAaOBHd7/Mzx56BRElk+m1px8gaoUjhYISRcIHPjCfa6+chu0sNVRn29hi2tI8/dxOvvu99YRhSLZZiPtZ+HEkTDX5ozun+IHHDSvmcNM1M5ByhK3YU5b9rKiVpG8oxxtE19/wOp5M1dCenBPgeDesFVa2JHll2wFW//sWXnpp32Hp0j3bpb6vUUuiEIFKRcnnYeKkNn7nw+dxzqwR2I6haeVuY4tpSbFjVxff+/5mXn5pH+k0pJJuC3es4o+ayqiN21qlUHCOwXnzxnHbzXOYMrnNlblJY/MQTwRVVBJGqNg3RNet2I8nIzTSIWOAGmzsyqkwhnWb9/Czx15j27Z9VCoQJKi2fD96Mqx1FTSVijvEYdToDFcsm8b7lk8l4ZshLw+vSTF8w5qndvDQI6+yc0cHCiQT4PtUw8g941ZVohjCCoQhpNOGWbNGc9Xl0zlv7kgILbYYnpbsZ1VUfBFifUd0/YocIhlOUdaLtdWuhtVy8e1vdrBh825efnU/e/Z0kctXiGOqp+85B1EQCMPa0kya2M7C+eNYMG80TdmEKxyxp2arVj9sIpskrkT88uV3WL9pF69tP8CBQ3lKpRi1PSVuvg/ZTJIxY1s5Z9YoFswbw8SJrWAtmg8BhiwLuF9wZct50XUrQgT/VB9YVk+XTvuQ8CC0dHSU2HewQHdniXIlxojQ1BTQNizN6PYmks0JQKEQYSPbsMYKAxp3rfAjHYBniIsh73QUOdRRolR0DJlIeDRnUwxvS7tmEJ64I27L0Wmpau4Tzisdin1+hR1q0X88WFWwbqXju/oBvKqyr0XQYncodK0v76nIpD0RamFuU4tg+ob66RauKNMFonrlCpwpeRY1qNazgk8fjAhUXcEaWTQ8uo+BiPvnjFg5VfQei4YxWjl83I7WckYw6/HgixCfDhXQFxpdlXOqcKrTvBsCJ6wig1AekqjDb3CGQwAqBqWIcfrgdA/pNzg1UKXWYL5gULo5g3Trb3CK4GjebUA7XO+vd1OC829wUhCtpoXRYRDZg6FBweDf4F2BapY2yl6D6o5q97/fsMCvC4SaBHjbILzxG9L/GsKlObzho7xKXCuUfvfgcItFe/49zczc4w84o30DLqZtedXH8hqVOBQxweksdNNadZD70YOqn1pqseDqS4z0uF4BjNSzbN3f9fz94Tc64gb9fuReX6xdspbeXP+9+rNWDVWtXzgqzF0d5ulyeokYQ9mGxLzmo9EbaLCPhIzXija8K0hvHDkRUiOkMYgx4Bk3KQZcXwtbTZ+NIAyJw4gwigjDiEolohLGRJEljGLK5YhKaIliSxRZypW4+ur5nvsZE0aWOK6eEm6tK/SsjstFF93YjAhiDJ5nCAKfwPfcz8DVN6SSAelUgnQ6STrlV//fJ50KSCY8UkkPL/Bc2VctV0GppQRDrKi1Pd1CToEnVMFKIIaK7iWWN1w26LoVa8j4yzQfnkRTyCNu1CtfXkTcyZ2+515GXLw3itBSmUKhRHd3ge5ciXyhQle+QrkC+RKEsQ9eExFpxM/gBc2I34SaJF6QwfgpjAkQL4nxEiAeIh7G8xHjYYwHIr1q8SxKdeJtTBxHxFGFKKoQhxXCsERYLlEpFwgrRcJKiVIxR7mYo1IqUCx0UynnKRfzVEoFogiiiqOpMRD4Lq8hkYBMEzRnfFqzaYa1ZRjenmHk8CwjhzczfFiGtpYUkvRc8MtqtXzO1rOkhqSNDtXTRfLR47Lo3uXVyiDdhG+WCSdbGqb1ztgSeEjCd7MSRlS68uw/0Mm+/Z3sPZDnUGdId8kj1AwEbSQyo0hnx9LSPoGmCaNoHTaacS0jaG4dQVOmjXSmhUQyjR8MsnFhg2DjClFYplzMU8x3UMh30nlgFx0HdpPrfIdc1zvkug5RKuYo5rvJdR9ib76bN9/polTcQ6W0HY3cOmjNwvixWaZMGsnUSe1MntDO8OEZTNJ3mS8VF/ZGqkGzBkAQ1zZO2Aj1LmDmWVxlykAbggM9hDcJz1W4hsqBfYfY/vputr/1DvsORBTiLInsRNpGLWHkhNmctfhsRo6dStuIcWRb2wn8/gqeHr1a/b/qewMe9vHRax7cyVjO5jBegoSXIJHKkh02pp9DjqmUi5RLOQq5Qxx6Zxf7frWdN7dt4MV1j/LCI6+h9nUCA6NHwOwZo5l/7mTOnjaaZEsK4hgtRaiefPKLqoq4gtXnoGrO6C9vmkYlfhnXMmZAB66pKuJ7EBj2787xzLrtbPzl23SVMwwfP58Z85Yxfe7FTJp2Lu0jjj1hqrbaj79HIfYYddWQ6mk3q/UIXutVnXy4cdNTCn+CPNs4KnNo/04KuUPs3rGN7Vuf56VNP2fXm5tp8mPec+4oLrtoFtOnD3dlZKWQwe4wlHrxZ4R6s2TR3dtFe46F2UzKn6vFqN8tYlQVSfgcOljgJw+8xJPP7GDE+BlcftN/YfGlNzNy3FlH/Y21cb0wsLaqarHz/7zoZfyqur1OtVTceH1Lvj07XmL9z+9m7QP/H796/RXmzGjipuvmc845o6s9COyADUZVtZL2DcXoRRYtPA9Wqeiapb4sXxvp+uv/TrOJT0lXGNOPBpGqCr5HZ0eRO7/9FNvfyPH+j32W93/8qwTJTPU7Fq2W1oiYd2Wsf8hRZ4ia0awYr2f6bVxh3c9/wt3//DW2b9nCFUsn8OGV82hKB64B58DmNNKWwJOu8L/Jons/o2uW9jp5wXo/lUhFVfttY4kRymXL22/nuPi91/Bbf/jNOvHBiT9jvGoXSou1MTaOjv2yMdbG1a2RrauFenVtXUX0VNq+61FbHMZgPK9OfFWLjSOMl+D85R/gq99bz0c+czuPPrmTv/5vvyCfD8EzA3LdqKqRSAXDT+u3r3cJfebqFnz/VXxvVH9rBNypIAk2bniLux/bz+RzrmHu+VczbdZCWoaNJEikBjEjg0Fv/0KPkj4qxWEwrsLjrLCjpqiWD3gcDDjtQhVrY4xxzLFuzQ+480sf4arLxvGJjy1BS2G/pIAqKoERQruXODxbLniwS7X6dPUjYtZd/wPNJj4o3f1TA+7CiqQCug50s+mXb7Jxyzvs7wqwphnxUiTSWZKpZtKZVtLNbfhBEs94BMkkqVQTmWwbTZkWkqkMqUwrTZlWUulm/ESaRCpNIpHG8xMYz3eTYAQRr9pY+ozuZjdk+Om/fY0f/f1X+Ns7rmL4iKM7oB4DkWYDT3LhD2ThvR+t0dwReWX1K5YfSawfGkinMBFXEt7SmuGy976Hy5Zbcu90snd/FwcO5ensfodiaTeFYpnywYgwiunKVzjYUaRUgs4cFKvnBqRTzm1gAT9IEiRS+H4CL0jgeT7G+ISRJQgCgkQC4wUY44N4ID6e5yOej+/7pFMpPN+tGs8Leq7jB/h+QBAkejFWgOf7eJ773L3cPT0/wPOCnver75nqeIznufe8oOpwstTORHCHZB6p1pwas1X7SK3F2ghrLbVdRc12staiGruf1qlQqakMDw515Bk+OuNsgRMIbFU1Equg3NWb5tVVvtrlWxseJR/ukIQ3cSDNoo0Rl9HbXUQEmlszNA9vYZox9GQb9UqZVoXQeb3yhQqd3WVUoFgo8y8/2cSv9uSAMpVSue5iR13jxwve085lF04hqLpW4zgiDEtUQutcxGHMr/Z08fgT+yiWqhL8CDeBKpSr3jvfc+1oasb4Ebu5akbyYWGIw15U3bem1wV6rPxe7u8jXRW9nuuoz/v6/YjwRXOzoa3abv+ExAcrCc9QiN4Gfcw93OqedvEiqK5Z6sui+wr6/Iof0eR/XjorlgHEBXr7sTWyEMXHNVBq5+1kmgMyLQkwwtq1r7F3f94RV1zbVndtoRxazl8whk98aBFBc8pRryeqUmUuAV94cf0Ont58CJOoicZeE6SuLPvS8yeDEV7dfoBd+7rJ5UI8D1IpH+HwotW63u5FCT2MKkocRYfPR6/b1hnlyG/09d4x/leqCRueEfIFy7Qp7YwY3VLtg3Dsea5extLkG7oqP5KF9xVqOz/oreeXLbOwFmLzT+TCzyoMutSynhN/ogtolVkECoUKm7buIYyURCCHxRHKFcvcs0fw0VvPIwgMNl/q6cFT/6cHW7ftJV8ISQSHN3py11KuXDyZ224+t36ewJ793WzZtp91L+zildcOYhXSKRlA95ITPWtfFznSqdTH9/oIWsbqRNo1y6ZD9cylE6lrBU9yYQTePwE9tKbXCnenSt1u5IJ7thLbn0mzL6p6wtOnTx7uXN59B/Ls2N3piiypER8qoTJhbDMfef88si0pNLZVQ1DqETtjel4A3fmyqy3sBRHXQHrcqCYuv/gsNI6Jc2VQZcyYVq644my+9OlL+eNPXsicGcPJ591Bj/1zveoJXo2B5wm5vHL5hROZPXcsWjpxDyRVjaXZFyL7syNPC4EjRfzqre5qnnzLJYmcIs+NEbpyZXL5EGN69LC10NIccMvVsxk5psUdJNWPIRWL4VHv1STK8oumMmZsC0S23oxBwwibr6Ch5ZxzxvDFT1/C731gHsmET7GkQ9KubaAwRigWlbMmNXPbTfOqlUj9GZdIlZbfAnpoXLvuYV+9bXWst99umH/vI+Tj52nyRTkFUkBhZ/UgpRqBRYQwhEsWT+K888ZjK1G/VqPxDKlUcLj+FCGKYcLYZhbMHVN3w/b+3EkVsMUQDS3Llk/nK390GWdPbaM7f2oqkI8FERccTCY9/o8PLSTVlIDoxFs/RWOafCEfP8999z6qt99+1BnCRxt5d2wVEZRAvy5m6FNFRQStxOza231YYkQcKWNGpblwwUTQgfWv8V0DpMNgLUwe38aw1jTEeszJqzNCd4Uxo1v44qcv5bIl48mdJiaoZQ4VS8pHb5nLhKnDscfpfXwYFMQgGP26rMJyx9aj/ugoBhBZHavebpi/8D/oDtdJk+8NlRRQd0MqYURHV+lwoohb/ePHtVYdHf3ydoEnZJsTh11LVfF9mD6lHQm8frV3MZ5gy+5o2N//2PmseO9Zp5wJRJy7vTun3HrtDC66eJprhtGPMdTPDs5Vnufehf/hdP/RZwf3vc1bvVVEVlkMf3byj3HcUYJAJYwplaP6ji6MYNSIJpbMn1ALWPf/giKMaG+qbiGdSrEW2rJJzpo0bEDDM0acA6YccdvK+dxyzYxTpg5cdbwz+m69djo33jDXdRQZ6L1FviKrVtkjdX8NfTKA3LY61rtWerLovp+Rj+6T5sAbsh2BEfKFkFy+Um9RZS2cO3M0I0Zk3EEPA7RF21vT9cbMNf05cnhTXfwPJPQsIhgFW6hw003ncuu1M4ZcEhjjknbLZeUjt8zhphvnYYtRvyv4nOUfeBTie2XRfT871snhcAJHj4Lg2S9SthU8GYK8G0ehQx1Fcnl3XEscK8NaAxadO67qRRxo8ARasymSCZ9a71OrMH5MK03NCdfqZaC0E5eSZQsVbrrxXG66ahrduaFhAmPEGcMIf/g7C7nqfbOwxUr/iQ/qOpLYCqJf1BNw+zEZQG5bHaMrjSx84CXK9huSTXiiDIkU2PNOjkpoMeI4f97sMUyd1Fa1dAcyyQKqpJI+qZRfjx4HPkyd2FZtQzJ4HhYcE9xy8zyuu3xKw5nAM0KprDSnE3z+kxdy/gWT3fmFA5gDUWLJJjzK9huy6L6X0ZVHWf69cQJX72qrerthbOov6KxsI+X5qke6WE4SAqVy5OoUVMlmfC5ZNAmvj2Pe+otE4NXtC6tKOu0zbnSWkxVgzuPsjMMPrJzPVZdOpCvXmDa4nicUSsqo9jR/8pmLOXvWGGyuPCAGU1VLyvPprGzD6F+6Y2FWH5dex2UAEZTVW0Umri4i/AECmEaqAQGrdHWX68GemdNGcNaU9kGs/qrbKrY0NycYNypb7T4O40ZlGT0i4/T/Sfq2REAUtBLz0Q8s5MqLJ9LZfXLOopqHb9yoDF/41MWMHdeGzZcxZoDhboPbL8f8gSy6r+CM+ePT64R3kNtWx6orPVl472Pk429KS9JDiU70dwOB5zmuSqc8lsyfgOnnVq0vqCp+KmDGWe31SOCUCW2kM0k0bkw/3HqEMbJ87EMLuWbZZLpyOuA8fqHneJsZU1r54qcvZsTI7OD6ByqRtCQ98uE3Zcm9j6ke2/DrjX7eZbXVu1Z6DAu/TGdlExnfb8SuoDaRrlIHZs8YwewZIwe1+g+/MIwb3ULgC8bApPGtgzMoj3cLFzJEw5gP//YCbltxNsWSa2jZH5VgjFuand3KhQvG8PlPXUxbaxO2H/79I6GqMRnfp7uyifOb/sSdAnd80V8fR3++JIKyco7K2Q+W8fgwkc3jG2lEWxmNYnL5MoEPFy2cSLo5yckdXeDUyujhGbKZBOmUx8SxrUOSQijiSmm0FHHDirl85vcWkc0k6c65m3n1oFWPR68WtCoUFVXhg++fzac+voR0wkf76e7uDVUU3wihzRPxYZHVFVbO0ROJ/hr63SbORQtXeiKrt+jz131CmhP/RiGK0MEdMe965wlhJebAoQKTx2eZPd2t/pOOQVmlOZMgCDyGD2tizMiMq8UbithWlbg2X2HhokmcNXkYdz/0Cs9u2ElXzhL4rmsoAjZSKqFLPpk7czi3XjeHqTNGosXQubsHYUeIISbt+XRXPiHn37/F0WhVv6XzgIgnsjrWNUt9WXz/D/X569/DsOQX6aiEQDDgkQMYtwPo6Crz3kvOItWS6neS43GhEAQenhEmj28laEqglWhI09JrR84Ma2vidz+8kPddNo1nN/2Kl17dx/4DeaLY0tyUZNrkYSxZMIFzZ48BT3pcu4Mam4a0JgMOlf5aFt//Q12z1BdZPSD7bOCrd/naKhPc9yVdt2IarcEtdFQiRAZ4LQXf5/Udhxg5vIkLFkxwaWInSyTp+dHakmTWtBGnLqptBI1iNIwZN76Vm6cM4+ZSRFdniTCKyTYnSWSTTh2VIzQ6CT+CakRbIqCj8hNZfP8Xdc1Sn+VrB2yXDeruqgh33C68b2uSdOlRmoIL6QojpP8MpQoSGH754m5EhLlzx6CVfmW3nhgCcWR57a2DjB/dQnM2yalqhl1DvV6ydkCkALHW292elANJiWgJfPLRM5SSl/PQnDJ3rOq33u+NQY9C1XlHdcPVIzGJx0h6c8lFA2ICgNhavIHud/sLz9SbNJxO1PMH+1NsccKLEdHs+5TjLeSLl8vFD++r0WIwlxv0zItg9a6Vnix4cD+F+Goq8Ws0+/5AfQRDeUSKRva0Ex96EmYbQvyM71OJX+NQ5Wq5+OF9etdKb7DEh5M9J7AWNbzo/l9RKF9JOX7VMYH2nwmGkD7/qUoRVWvE305X/D5Z/uDO40X5+ouTXn51JrjwoTc5VLmccvwiLQkf9OjEvN9gcFCNaEn4hPGLdMpyufT+1xtBfGhQP6A6Eyx/cCf54hWUoidpSQSNdhn/WkKJaE34lONfsF/fK0vv2dEo4kMDG0LVmeDih/dxsPNK8tFdDEv4isY6WMf+rzHcJkJjhiV88uGPySWulPfeu7eRxIeT2AUcC73zznXDir8i5X+JUozGNhZpTAOq/+xQ1Vg845H2oBD9tSy894vu/cNz+huBITGTal1HRFZZffb6D5Ly/oHAZMkPfJv4a4eapR/ZHKXok3L+/f/q4vqD2+efCENqJ9e7jzy9Yh5p/idNwSLtqli3Jf41re0+BlTVIiCtCUMhWk/JflyW3Le5Gn8ZstqMISWCLF8b6Zqlvlx47wvsCi8hH/2tJH0jKd+gRL85pIJaMXEkKd9I0jfkom9xsPMSWXLf5qpvf0gLc07JTvkwu2D9je8jkG+SNrPpClGrv7a2garGYsQjG0Ax2kIU/7EsvP8h91nj9X1fOGWuEmcXrDQiq2O9+4Ysk/TP8MxnSZqkdocWQRvVpfRMRy2vUrKBoWJLxPZb7Ct9Vd73cF7VJXMMhb7vC6fcV9Z7G6PPXTufwP8LEmYFCFoI3cT8J7UPVNXZP5nA1a6F9m7K9g5Zct9mOHxuThVOi7O0tzQA0I03XovRLxN4lwBoLlQEi0i1jcS7Fwqu5wuINPkGIxDap4j5mrznngcATvWq743TOrlue+OyjQB00w03I/wRxlxKIJCLACJFzVAcbT+UUNQKYgGfjO+ikqE+hcg35Ly7fwJHP//pwBmxuo4UfbpxxZUgnwKuI+P7lGK0HFsRsap4jQisDQVUURFiVTWS8AxpD82FVow8gDF/L/PurvfnOx3ivi+cUROpd630WNkjCnXTzXMh/giWW0l5Z+EJFGM0rDGDus7+p4khquJda2ORwBGdWKEcv4GRHxPH/yoLnI4HJ+6Hems3EJxRDFCDY4Q5WlcN665vwveuwNpbEXkvCTOOwEDFulO53VbS9blWMX32XzrZMVHtFSVqBVFVFTHikfQgYSC0ULG7Mfowln/HlB6R8x7OQ1XUr94qZ8KKPxJnJAPU4HTkVum9YnTjjW14XESk16C6FJhFcxBgxGUUhxZCrW616j3lpdpFTODYiTl1x1Qt4b3HKBMRMfjGEdt3mUaaC2OBrcDP8XgQY38h8+4/VL/emqU+y5bZ06njT4QzmgFqqO0awGUmH/bZ+humI7oYlfNRex7IdERGk5BEPRfPqus+abXnPJ96A0JqSfvup5Hqq/q74kR6JQ6BfVjdjmEDnnkWzAaZf/e2w8e6surLOD1W/UDxrmCA3qgzw+P7pNbr7rDPn7whS0qmQDQdZCZGJmOZDIxGGYaQBdJAQrXeJzECKkAR6AI6gL0Y3sLqW/jmFVTeIM6/IYse6TzqnmuW+iwbpe8WovfG/w/NZhhCRsi3JgAAAABJRU5ErkJggg=="

post_example_unfilled = {
    "type": openapi.Schema(type=openapi.TYPE_STRING),
    "title": openapi.Schema(type=openapi.TYPE_STRING),
    "id": openapi.Schema(type=openapi.TYPE_STRING),
    "source": openapi.Schema(type=openapi.TYPE_STRING),
    "origin": openapi.Schema(type=openapi.TYPE_STRING),
    "description": openapi.Schema(type=openapi.TYPE_STRING),
    "contentType": openapi.Schema(type=openapi.TYPE_STRING),
    "content": openapi.Schema(type=openapi.TYPE_STRING),
    "author": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
    "categories": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
    "count": openapi.Schema(type=openapi.TYPE_NUMBER),
    "comments": openapi.Schema(type=openapi.TYPE_STRING),
    "commentsSrc": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
    "published": openapi.Schema(type=openapi.TYPE_STRING),
    "visibility": openapi.Schema(type=openapi.TYPE_STRING),
    "unlisted": openapi.Schema(type=openapi.TYPE_BOOLEAN)
}

like_example_filled = {
    "type": "like",
    "@context": "https://www.w3.org/ns/activitystreams",
    "summary": "Lara Croft Likes your comment",
    "author": {
        "type": "author",
        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Lara Croft",
        "url": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "object": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
}

like_example_unfilled = {
    "type": openapi.Schema(type=openapi.TYPE_STRING),
    "@context": openapi.Schema(type=openapi.TYPE_STRING),
    "summary": openapi.Schema(type=openapi.TYPE_STRING),
    "author": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
    "object": openapi.Schema(type=openapi.TYPE_STRING),
}


# Be aware that Posts can be images that need base64 decoding.
# posts can also hyperlink to images that are public


#  https://www.django-rest-framework.org/tutorial/3-class-based-views/
class PostList(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/""" 

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "type": "posts",
                        "items": [
                            post_example_filled
                        ]
                    }
                }
            )
        }
    )
    def get(self, request, id, format=None):
        """GET [local, remote] get the recent posts from post AUTHOR_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        posts = Post.objects.all().filter(author=id)

        if not request.app_session or request.app_session.author != author:
            posts = posts.filter(unlisted=False)

        posts = posts.order_by("-published")
        posts = paginate(request, posts)
        serializer = PostSerializer(posts, many=True)

        authorData = AuthorSerializer(author).data
        serializedPosts = serializer.data

        for p in serializedPosts:
            p["author"] = authorData
        dict = {"type": "posts", "items": serializedPosts}
        return Response(dict, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=post_example_unfilled
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    def post(self, request, id, format=None):
        """POST [local] create a new post but generate a new id"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        d = request.data
        self.fill_optional_values(d, id)
        d["author"] = id
        serializer = PostSerializer(data=d)

        if serializer.is_valid():
            post = serializer.save(id=d["id"])
            # add the post to the inbox of each of the author's followers
            add_data_to_inboxes_of_author_and_followers(author, post)
            return Response({"id": post.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def fill_optional_values(self, data, authorId):
        postId = generate_random_string()
        if "id" in data:
            postId = data["id"]
        else:
            data["id"] = postId

        if not "source" in data:
            data["source"] = get_host() + "authors/" + \
                authorId + "/posts/" + postId
        if not "origin" in data:
            data["origin"] = get_host() + "authors/" + \
                authorId + "/posts/" + postId
        if not "comments" in data:
            data["comments"] = get_host() + "authors/" + authorId + \
                "/posts/" + postId + "/comments/"


class PostImage(APIView):
    """Creation URL ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": post_example_filled_img
                }
            )
        }
    )

    def get(self, request, author_id, post_id):
        """GET [local, remote] get the image contents of a post, or return a 404 if the post is not an image"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(
            Post.objects.all().filter(author=author_id), id=post_id)
        if not post.contentType in [ContentType.JPEG, ContentType.PNG]:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(base64.b64decode(post.content),
                            content_type=post.contentType.split(";")[0])


class PostDetail(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": post_example_filled
                }
            )
        }
    )
    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the public post whose id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # id is unique (don't need author_id)
        post = get_object_or_404(Post, id=post_id)
        post_serializer = PostSerializer(post).data
        author = AuthorSerializer(author).data
        post_serializer["author"] = author
        post_serializer["count"] = len(Comment.objects.filter(post=post))
        return Response(post_serializer, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=post_example_unfilled
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    def put(self, request, author_id, post_id, format=None):
        """PUT [local] create a post where its id is POST_ID (must be authenticated"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Post, id=post_id, author=author_id)
        request.data["author"] = author_id
        # overwrite post with request.data
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id, post_id, format=None):
        """DELETE [local] remove the post whose id is POST_ID"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_200_OK)

##################################################################################################################
#                                               COMMENTS                                                         #
##################################################################################################################


class CommentList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    {
                        "type": "comments",
                        "page": 1,
                        "size": 5,
                        "post": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                        "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                        "comments": [
                            {
                                "type": "comment",
                                "author": {
                                    "type": "author",
                                    "id": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                                    "url": "http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
                                    "host": "http://127.0.0.1:5454/",
                                    "displayName": "Greg Johnson",
                                    "github": "http://github.com/gjohnson",
                                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                },
                                "comment": "Sick Olde English",
                                "contentType": "text/markdown",
                                "published": "2015-03-09T13:07:04+00:00",
                                "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                            }
                        ]
                    }
                }
            )
        }
    )
    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] get the list of comments of the post whose id is POST_ID (paginated)"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get the post
        post = get_object_or_404(Post, id=post_id)
        # get all comments for the post
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        dict = {"type": "comments", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING),
                "author": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                "comment": openapi.Schema(type=openapi.TYPE_STRING),
                "contentType": openapi.Schema(type=openapi.TYPE_STRING),
                "published": openapi.Schema(type=openapi.TYPE_STRING),
                "id": openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    def post(self, request, author_id, post_id, format=None):
        """
        POST [local] if you post an object of “type”:”comment”,
        it will add your comment to the post whose id is POST_ID
        """
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post exists
        post = get_object_or_404(Post, id=post_id)

        # add ids to request.data for serializer
        request.data["author"] = author_id
        request.data["post"] = post_id
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save()
            # add the comment to the inbox of the post author and all of their followers
            add_data_to_inboxes_of_author_and_followers(post.author, comment)
            return Response({"id": comment.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##################################################################################################################
#                                               LIKED                                                            #
##################################################################################################################

class LikedList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/liked"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    {
                        "type": "liked",
                        "items": [
                            like_example_filled
                        ]
                    }
                }
            )
        }
    )
    def get(self, request, author_id, format=None):
        """GET [local, remote] list what public things AUTHOR_ID liked."""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get all of the author's post likes
        post_likes = author.post_likes.all()
        serializer1 = PostLikeSerializer(post_likes, many=True)
        # add all of the author's comment likes
        comment_likes = author.comment_likes.all()
        serializer2 = CommentLikeSerializer(comment_likes, many=True)

        # TODO: Figure out how to properly combine two serializers
        arr = []
        for serializer in [serializer1.data, serializer2.data]:
            for data in serializer:
                arr.append(dict(data))
        return Response({"type": "liked", "items": arr}, status=status.HTTP_200_OK)

##################################################################################################################
#                                               POST LIKES                                                       #
##################################################################################################################


class PostLikeList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    {
                        "type": "likes",
                        "items": [
                            like_example_filled
                        ]
                    }
                }
            )
        }
    )
    def get(self, request, author_id, post_id, format=None):
        """GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID"""

        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Post, id=post_id)
        likes = post.likes.all()
        serializer = PostLikeSerializer(likes, many=True)
        dict = {"type": "likes", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=like_example_unfilled
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    def post(self, request, author_id, post_id, format=None):
        "POST a like for a particular post"
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post and comment exist
        post = get_object_or_404(Post, id=post_id)
        # save a new like for this post
        like = post.likes.create(author=post.author)
        # add the like to the inbox of the post's author and all of their followers
        add_data_to_inboxes_of_author_and_followers(post.author, like)
        return Response(status=status.HTTP_201_CREATED)


##################################################################################################################
#                                               COMMENT LIKES                                                    #
##################################################################################################################

class CommentLikeList(APIView):
    """URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                    {
                        "type": "likes",
                        "items": [
                            like_example_filled
                        ]
                    }
                }
            )
        }
    )
    def get(self, request, author_id, post_id, comment_id, format=None):
        """GET the likes on a particular comment"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # get the comment we're looking for
        comment = get_object_or_404(Comment, id=comment_id)
        comment_likes = comment.likes.all()
        serializer = CommentLikeSerializer(comment_likes, many=True)
        dict = {"type": "likes", "items": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=like_example_unfilled
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            )
        }
    )
    def post(self, request, author_id, post_id, comment_id, format=None):
        """POST a 'like' to a particular comment"""
        # ensure author exists and is authorized
        author = get_object_or_404(Author, id=author_id)
        if not author.isAuthorized:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # ensure the post and comment exist
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        # save a new like for this comment
        like = comment.likes.create(author=author)
        # add the like to the inbox of the post author and all of their followers
        add_data_to_inboxes_of_author_and_followers(post.author, like)
        return Response({"id": like.id}, status=status.HTTP_201_CREATED)
