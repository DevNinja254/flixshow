from django.shortcuts import render, redirect
from Members.form import Messages, DepositForm
from multimedia.form import VideoUploads,VideoForm
from django.contrib.auth.decorators import login_required
from .DRY import userDetails
from multimedia.models import videos as Videos, HomepageVideo, VideoUpload, Cartegories
from Members.models import DepositHistory, DownloadHistory, Buyers, Cart,Message,Members, Onwatch, Payment
from.stk_code import sendStkPush
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json

# Create your views here.
def home(request):
    # call userdatails function then pass request arg to fetch user details
    userDetail = userDetails(request)
    # get video name to display in the homepage background
    homepageVideo = HomepageVideo.objects.all().values()
    videoName = ''
    # loop to get the videoname
    for vidzName in homepageVideo:
        videoName = vidzName["videoName_id"]
        break
    # fetch videoDetails with that name and create an object of it
    videoDetails = VideoUpload.objects.filter(title = videoName)
    videoObject = ""
    for vidx in videoDetails:
        videoObject = vidx
        break
    #GET all cartegories cnvt to string
    cartegoris = Cartegories.objects.all()
    cartegories = []
    for carties in cartegoris:
        carties.cartName = str(carties.cartName)
        cartegories.append(carties) 

    # fetch all videoDetails object convert type and display to string
    allVideoDetailed = VideoUpload.objects.all()
    allVideoDetails = []
    for allVideoDetail in allVideoDetailed:
        # print(allVideoDetail)
        allVideoDetail.cartegory_id = str(allVideoDetail.cartegory_id)
        allVideoDetail.display = str(allVideoDetail.display)
        allVideoDetail.popular = str(allVideoDetail.popular)        
        allVideoDetails.append(allVideoDetail)  
    if userDetail["buyer"]:
        is_approved = userDetail["userMembDetailsDic"]
    elif userDetail["seller"]:
        is_approved = userDetail["userMembDetailsDic"]
    if userDetail["logged"] == True:
        context = {
            "username": userDetail["username"],
            "email": userDetail["email"],
            "videoObject":videoObject,
            "cartegories":cartegories,
            "allVideoDetails": allVideoDetails,
            "is_approved":is_approved,
        }
    else:
         context = {
            "username": "username",
            "email": "email@gmail.com",
            "videoObject":videoObject,
            "cartegories":cartegories,
            "allVideoDetails": allVideoDetails,
        }
    
    return render(request, "homePage.html", {"context":context})
@login_required(login_url="/membership/login/")
def moviesAndSeries(request):
    userid = Members.objects.get(email = request.user)
    userExist = Buyers.objects.filter(members_ptr_id = userid.id)
    if userExist.exists():
        is_buyer = True
        user = userDetails(request)["userBuyrDetailsDi"]
        videoTitle = request.GET["videoTitle"]
        videoDetails = VideoUpload.objects.filter(title = videoTitle)
        # loop through and get the first videoDetails Object
        videoDetail = ''
        videolity = ''
        for video in videoDetails:
            video.Quality = video.Quality.strip().upper().split(" ")
            videolity = video.Quality
            videoDetail = video
            break
        # Fetch whose name == videoTitle change all data to arrayString
        vidz = Videos.objects.filter(name = videoTitle)
        vidzUpdate = []
        for vid in vidz:
            vid.quality = vid.quality.upper().strip()
            vidzUpdate.append(vid)
        carty = Cart.objects.filter(username = user["username"])
        cartExist = False
        for cats in carty:
            if cats.video_name == videoTitle:
                cartExist =True
        # treding video
        allVideos = VideoUpload.objects.all()
        popularVid = []
        count = 0
        for vida in allVideos:
            if str(vida.popular) == "True":
                popularVid.append(vida)
            if count == 5:
                break
        context = {
            "videoDetails":videoDetail,
            "video":vidzUpdate,
            "videolity": videolity[0],
            "user" :user,
            "cartExist": cartExist,
            "trending":popularVid,
            "buyer" : is_buyer,
        }
    else:
        is_buyer = False
        context = {
            "buyer":is_buyer
        }
    return render(request, "mp4.html", {"context":context})

 

@login_required(login_url="/membership/login/")
def admins(request):
    userDetail = userDetails(request)
    messages = Message.objects.all()
    payments = DepositHistory.objects.all()
    download = DownloadHistory.objects.all()
    watch = Onwatch.objects.all()
    context = {
        "username":userDetail["username"],
        "is_approved": userDetail["userMembDetailsDic"]["is_approved"],
        "messages": messages,
        "payments":payments,
        "downloads": download,
        "watch":watch
    }
    return render(request, "admins.html", {"context": context})

def message(request):
    if request.method == 'POST':
    #   detailed form
      form = Messages(request.POST)
      if form.is_valid():
         form.save()
         return redirect("/")
      
    else:
        # blank form
        form = Messages()
    return render(request, 'message.html',{'form': form})

@login_required(login_url="/membership/login/")
def addVideo(request):
    userDetail = userDetails(request)
    if request.method == 'POST':
        uploadType = request.POST["upload_type"]
        print(uploadType)
        if uploadType == "video_details":
            form = VideoUploads(request.POST, request.FILES)
            if form.is_valid():
                
                form.save()
        elif uploadType == "video":
            print("video")
            vidz = VideoForm(request.POST, request.FILES)
            if vidz.is_valid():
                print("valid")
                for fila in request.FILES.getlist('video'):
                    # Handle the uploaded file (e.g., save to storage)
                    print(fila)
                    Videos.objects.create(
                        name = request.POST["name"],
                        video = fila,
                        quality = request.POST['quality']

                    )
                

        context = {
                "form": VideoUploads(),
                'videoForm': VideoForm(),
                "username":userDetail["username"],
                "is_approved": userDetail["userMembDetailsDic"]["is_approved"]
            
            }
        return render(request, 'addVideo.html', {"context": context})
    
      
    else:
        # blank form
        form = VideoUploads()
        videoForm = VideoForm()
    context = {
        "form": form,
        "videoForm": videoForm,
        "username":userDetail["username"],
        "is_approved": userDetail["userMembDetailsDic"]["is_approved"]
 
    }
    return render(request, "addVideo.html", {"context": context})


def play(request):
    nam = str(request.GET["name"]).strip()
    videoName = request.GET["videoNae"]
    vide = Videos.objects.filter(name = nam)
    otherVideos = []
    count = 1
    playVideo = ''
    ended = []
    endTrue = 0
    endFalse = 0
    for vi in vide:
        if videoName == vi.video:
            vi.quality = str(vi.quality).upper()
            playVideo = vi
        ended.append(vi.ended)
    vided = Videos.objects.all()
    for ends in ended:
        if ends:
            endTrue +=1
        else:
            endFalse += 1
    print(endFalse, endTrue)
    for viz in vided:
        if count <= 10:
            otherVideos.append(viz)
            count += 1
        else:
            break
    
    # fetch all watch videos
    onWatch = Onwatch.objects.all()
    if endFalse == 0:
        for onwat in onWatch:
            if onwat.name == videoName:
                onwat.delete()
    titles = []
    for wat in onWatch:
        if wat.watcher == userDetails(request)["userBuyrDetailsDi"]["username"]:
            titles.append(wat.video_name)
    
    context = {
        "videos":vide,
        "playVideo":playVideo,
        "quality":str(request.GET["quality"]).strip().upper(),
        "otherVideo":otherVideos,
        "titles":titles
    }
    return render(request, "play.html", {"context":context})
@login_required(login_url="/membership/login/")


def deposit(request):
    
    userid = Members.objects.get(email = request.user)
    userExist = Buyers.objects.filter(members_ptr_id = userid.id)
    if userExist.exists():
        is_buyer = True
        user = userDetails(request)
        if request.method == "POST":
            Amount = str(request.POST["amount"])
            number = str(request.POST["phoneNumber"])
            phoneNumber = "254" + number[1:]
            stk = sendStkPush(Amount, phoneNumber)
            # print(stk)
            depoExist = Payment.objects.filter(phone_number = phoneNumber)
            if depoExist.exists() == False:
               Payment.objects.create(
                username = user["username"],
                phone_number = phoneNumber
            )
            return redirect("/membership/dashboard/")
    else:
        is_buyer = False
    context = {
            "buyer":is_buyer
    }
    return render(request, "deposit.html",{"context": context} )

def download(request):
    if request.method == "POST":
        videoTitle = request.POST["videoTitle"]
        user = userDetails(request)["username"]
        # print(user)
        price = request.POST["price"]
        # remove item from cart on download it the item exist in cart table
        existCart = Cart.objects.filter(video_name = videoTitle)
        if existCart.exists():
            existCart.delete()
        # save download details to downloadhistory table
        DownloadHistory.objects.create(
            name = user,
            video_name = videoTitle,
            cost = price  
        )
        # deduct payment from user Account
        userAccount = Buyers.objects.filter(username = user)
        if userAccount.exists():
            for use in userAccount:
                use.account = int(use.account) - int(price)
                use.save()
                break
        # userAccount.account = int(userAccount.account)
        
    return redirect("/membership/dashboard/")
@csrf_exempt
def stkCallback(request):
    callback_data = json.loads(request.body)
    # print("hello", request.user, callback_data)
     # Check the result code
    result_code = callback_data['Body']['stkCallback']['ResultCode']
    if result_code != 0:
    # If the result code is not 0, there was an error
        error_message = callback_data['Body']['stkCallback']['ResultDesc']
        response_data = {'ResultCode': result_code, 'ResultDesc': error_message}
        return JsonResponse(response_data)
    callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']
    amount = None
    phone_number = None
    for item in callback_metadata['Item']:
        if item['Name'] == 'Amount':
            amount = item['Value']
        elif item['Name'] == 'PhoneNumber':
            phone_number = item['Value']
    # Check the result code
    result_code = callback_data['Body']['stkCallback']['ResultCode']
    paid = Payment.objects.get(phone_number = str(phone_number))
    # print(paid)
    if paid.payment_Suc == False:
        userAccount = Buyers.objects.get(username = paid.username)
        # print(paid.username)
        userAccount.account = int(userAccount.account) + int(amount)
        userAccount.save()
        DepositHistory.objects.create(
                amount = amount,
                name = paid.username
            )
        paid.delete()
    else:
        paid.delete()   
    # print(phone_number, amount)
    # Save the variables to a file or database, etc.
    # ...

    # Return a success response to the M-Pesa server
    response_data = {'ResultCode': result_code, 'ResultDesc': 'Success'}
    return JsonResponse(response_data)
login_required(login_url="/membership/login")
def cart(request):
    user = userDetails(request)["username"]
    if request.method == "POST":
        videoName = request.POST["videoName"]
        Cart.objects.create(
            video_name = videoName,
            username = user
        )
        return redirect("/cart/")
    userCart = Cart.objects.filter(username = user)
    Allcarts = []
    total = 0
    for cat in userCart:
        datails = VideoUpload.objects.filter(title = cat.video_name)
        for dat in datails:
            total += dat.price
            Allcarts.append(dat)
    context = {
        "allCarts":Allcarts,
        "total":total,
        "number": len(Cart.objects.filter(username = user)),
    }
    return render(request, "cart.html", {"context":context})
def removeCart(request):
    if request.method == "POST":
        videoTitle = request.POST['videoTitle']
        existCart = Cart.objects.filter(video_name = videoTitle)
        if existCart.exists():
            existCart.delete()
    return redirect("/cart/")
def activate(request):
    if request.method == "POST":
        userAccount = Buyers.objects.get(username = userDetails(request)["userBuyrDetailsDi"]["username"])
        videoDet = VideoUpload.objects.get(title = request.POST["videoName"])
        print(videoDet.price,userAccount.account)
        if userAccount.account < videoDet.price:
            return redirect("/deposit/")
        else:
            userAccount.account = int(userAccount.account) - int(videoDet.price)
            userAccount.save()
            Onwatch.objects.create(
                video_name = request.POST["videoName"],
                watcher = userDetails(request)["userBuyrDetailsDi"]["username"]
            )
        videox = Videos.objects.filter(name = request.POST["videoName"])
        for vid in videox:
            vid.ended = False
            vid.save()
    return redirect("/membership/dashboard")

def deactivate(request):
    if request.method == "POST":
        vide = Videos.objects.filter(video = request.POST["videoName"])
        vide.ended = True
        vide.save()
        print(request.POST["videoName"])
    return redirect("/membership/dashboard")
def search(request):
    searchTerm = request.GET["searchTerm"]
    videoDetail = VideoUpload.objects.filter(title = searchTerm)
    if videoDetail.exists() ==False:
        videoDetail = VideoUpload.objects.filter(cartegory = searchTerm)
    elif videoDetail.exists() ==False:
         videoDetail = VideoUpload.objects.filter(typs = searchTerm)
    context = {
        "videoDetail": videoDetail,
    }     
    return render(request, "search.html", {"context": context})
def cancelPurchase(request):
    videoName = request.POST["videoName"]
    videoExist = Onwatch.objects.filter(video_name = videoName)
    if videoExist.exists:
        for vids in videoExist:
            vids.delete()
    return redirect("/")
