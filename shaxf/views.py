from django.shortcuts import render, redirect
from .models import Wheel, Nav, Mustbuy, Shop, MainShow, FoodTypes, Goods, User, Cart, Order
# Create your views here.
import time, random
from django.contrib.auth import logout
from django.http import JsonResponse

def index(request):
    return redirect("/home/")

# 主页
def home(request):
    sliderList = Wheel.objects.all()
    navList = Nav.objects.all()
    menuList = Mustbuy.objects.all()
    shops = Shop.objects.all()
    shop1 = shops[0]
    shop2 = shops[1:3]
    shop3 = shops[3:7]
    shop4 = shops[7:11]
    mainList = MainShow.objects.all()

    return render(request, "shaxf/home/home.html", {"title":"主页","sliderList":sliderList,"navList":navList,"menuList":menuList, "shop1":shop1, "shop2":shop2, "shop3":shop3, "shop4":shop4,"mainList":mainList})






#闪送超市
def market(request, gid, cid, sflag):
    leftSlider = FoodTypes.objects.all()

    #获取展示的数据
    productList = Goods.objects.filter(categoryid=gid)
    #是否过滤子组数据
    if cid != "0":
        productList = productList.filter(childcid=cid)
    #排序
    if sflag == "1":
        productList = productList.order_by("productnum")
    elif sflag == "2":
        productList = productList.order_by("price")
    elif sflag == "3":
        productList = productList.order_by("-price")

    #获取子类名数据
    childList = []
    oneFoodType = leftSlider.get(typeid=gid)
    print(oneFoodType)
    # 全部分类:0#进口水果:103534#国产水果:103533
    cStr = oneFoodType.childtypenames
    # 全部分类:0     进口水果:103534      国产水果:103533
    arr = cStr.split("#")
    for part in arr:
        parr = part.split(":")
        obj = {"childName":parr[0], "childId":parr[1]}
        childList.append(obj)

    token = request.COOKIES.get("token")
    carts = Cart.object1.filter(user__userToken=token)
    for i in productList:
        for j in carts:
            if i.productid == j.product.productid:
                i.num = j.productnum
                continue



    return render(request, "shaxf/market/market.html", {"title":"闪送超市","leftSlider":leftSlider, "productList":productList,"childList":childList,"gid":gid,"cid":cid})







#购物车
def cart(request):
    token = request.COOKIES.get("token")
    carts = Cart.object1.filter(user__userToken=token)


    return render(request, "shaxf/cart/cart.html", {"title":"购物车","carts":carts})



#添加购物车
def addCart(request, flag):
    #验证是否登录
    token = request.COOKIES.get("token")
    if not token:
        #登录
        # response = redirect('/login/')
        # response.content_type = "text/plain"
        # return response
        return JsonResponse({"data":-1})

    #操作标志
    flag = int(flag)
    if flag == 2:
        flag = -1

    #商品id
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    #没有库存
    #增加商品时执行，减少商品时不能执行
    if flag == 1:
        if product.storenums == 0:
            return JsonResponse({"data": -2})

    # 获取当前用户对象  88888888
    currentuser = User.objects.get(userToken=token)

    #找可用的订单数据
    try:
        order = Order.objects.filter(user=currentuser).get(isActive=True)
    except Order.DoesNotExist as e:
        #增加商品时执行
        if flag == 1:
            orderid = str(random.randrange(1, 1000000)) + currentuser.userAccount
            order = Order.createorder(orderid,currentuser,1,True,False)
            order.save()
        #减少商品，返回
        elif flag == -1:
            return JsonResponse({"data": -2})



    #测试用的
    # cart = Cart.createcart(currentuser,product,1,10,True,order,False)
    # cart.save()

    #添加商品
    try:
        cart = Cart.object1.filter(user=currentuser).get(product=product)
        # 购物车里，二次添加，减少在这里减一
        if flag == 3:
            cart.isChose = not cart.isChose
        else:
            cart.productnum += flag
            cart.productprice = cart.productnum * float(product.price)
        if cart.productnum == 0:
            cart.delete()
        else:
            cart.save()
    except Cart.DoesNotExist as e:
        # 第一次添加，减少时退出
        if flag == 1:
            cart = Cart.createcart(currentuser,product,1,float(product.price),True,order,False)
            cart.save()
        elif flag == -1:
            return JsonResponse({"data": -2})


    #库存减1
    if flag != 3:
        product.storenums -= flag
        product.save()

    #返回
    return JsonResponse({"data": cart.productnum,"price":cart.productprice, "chose":cart.isChose})

#下单
def deal(request):
    # 获取用户token
    token = request.COOKIES.get("token")
    currentuser = User.objects.get(userToken=token)

    # 获取当前用户的所有购物信息
    carts = Cart.object1.filter(user__userToken=token).filter(isChose=True)


    if len(carts) == 0:
        # 如果没有信息，直接返回
        return JsonResponse({"data":1})
    #将购物车数的isChose变为False，isDelete变为True
    for cart in carts:
        cart.isChose = False
        cart.isDelete = True
        cart.save()

    #将该订单数据中的isActive设置为False，设置进度为2
    order = Order.objects.filter(user=currentuser).get(isActive=True)
    order.isActive = False
    order.progress = 2
    order.save()

    dcarts = Cart.object1.filter(order__orderid=order.orderid)
    if len(dcarts) > 0:
        #在订单中删除这些数据，创建新订单添加这些数据
        orderid = str(random.randrange(1,1000000)) + currentuser.userAccount
        neworder = Order.createorder(orderid, currentuser, 1, True, False)
        neworder.save()
        for c in dcarts:
            c.order = neworder
            c.save()


    return JsonResponse({"data": 0})



#我的
def mine(request):
    username = request.session.get(request.COOKIES.get("name"), "未登录")
    return render(request, "shaxf/mine/mine.html", {"title":"我的", "username":username})
#登陆
def login(request):
    if request.method == "GET":
        return render(request, "shaxf/mine/login.html", {"title":"登陆"})
    else:
        username = request.POST.get("username")
        passwd   = request.POST.get("passwd")

        # 根据用户名尝试获取用户对象
        try:
            user = User.objects.get(userAccount=username)
        except User.DoesNotExist as e:
            return redirect("/login/")

        #验证密码
        if passwd != user.userPasswd:
            return redirect("/login/")

        response = redirect("/mine/")

        #登陆成功
        #重新生成token值存储到数据库，并且写入cookie
        torken = time.time() + random.randrange(1, 100000)
        user.userToken = str(torken)
        user.save()
        response.set_cookie("token", user.userToken)

        #将昵称存储到session做状态保持，同时将session的键当值写入cookie
        request.session["username"] = user.userName
        response.set_cookie("name", "username")

        #返回到进入登录界面之前的界面

        return response

def quit(request):
    logout(request)
    res = redirect("/mine/")
    res.delete_cookie("token")
    return res


def register(request):
    if request.method == "GET":
        return render(request, "shaxf/mine/register.html", {"title":"注册"})
    else:
        if request.is_ajax():
            #验证账号是否存在
            userAccount = request.POST.get("userAccount")
            try:
                user = User.objects.get(userAccount=userAccount)
                #说明账号已被占用
                return JsonResponse({"data":1})
            except User.DoesNotExist as e:
                #说明账号可以使用
                return JsonResponse({"data": 0})
        else:
            userAccount = request.POST.get("userAccount")
            userPasswd = request.POST.get("userPasswd")
            userName = request.POST.get("userName")
            userPhone = request.POST.get("userPhone")
            userAdderss = request.POST.get("userAdderss")
            #文件上传
            userImg = "shaxf/"+ userAccount +".png"
            userRank = 1
            userToken = str(time.time() + random.randrange(1, 1000000))

            user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
            user.save()

            #注册成功需要写入session，做状态保持，默认登陆
            request.session["username"] = userName
            response = redirect("/mine/")
            response.set_cookie("name", "username")
            response.set_cookie("token", userToken)
            return response

# 详情页
def detail(request):
    token = request.COOKIES.get('token')
    user = User.objects.get(userToken=token)
    try:
        orderList = Order.objects.filter(user=user)
    except:
        return

    # 求每个订单的价格
    sum = 0
    for order in orderList:
        cartList = Cart.object3.filter(order=order)
        for cart in cartList:
            sum += cart.productprice
        order.price = sum

    return render(request, 'shaxf/mine/detail.html', {'orderList': orderList})

def allProducts(request):
    orderid = request.GET.get('id')
    productList = Cart.object3.filter(order__orderid=orderid)
    return render(request, 'shaxf/mine/allProducts.html', {'productList': productList})

def allOk(request):
    print('*******')
    # 获取用户token
    token = request.COOKIES.get("token")
    currentuser = User.objects.get(userToken=token)

    # 获取当前用户的所有购物信息
    carts = Cart.object1.filter(user__userToken=token).filter(isChose=True)

    if len(carts) == 0:
        # 如果没有信息，直接返回
        return JsonResponse({"data": 1})

    # 全选
    for cart in carts:
        cart.isChose = True
        cart.save()
    return JsonResponse({'data': 2})