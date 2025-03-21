from django.shortcuts import render, redirect
from Members.form import Messages, DepositForm
from multimedia.form import VideoUploads,VideoForm
from django.contrib.auth.decorators import login_required
from .DRY import userDetails
from multimedia.models import videos as Videos,AwaitingActivation, HomepageVideo, VideoUpload, Cartegories
from Members.models import DepositHistory, DownloadHistory, Buyers, Cart,Message,Members, Onwatch, Payment, Notification, Paymentcodes
from.stk_code import sendStkPush
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json, base64

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
    # latest videos 
    lates = allVideoDetails[-1:-21:-1]
    latests = []
    for late in lates: 
        if len(late.synopsis) > 50:
            late.synopsis = "{syno}[...]".format(syno=str(late.synopsis)[0:50:1])
        latests.append(late)
    if userDetail["buyer"]:
        is_approved = userDetail["userMembDetailsDic"]
    elif userDetail["seller"]:
        is_approved = userDetail["userMembDetailsDic"]
    # notitication 
    notifications = Notification.objects.all()
    notice = []
    for noti in notifications:
        notice.append(noti.message)
    print(len(notice))    
    if len(notice) == 0:
        notice = ['All updates, changes and instructions to be communicated here.']
    if userDetail["logged"] == True:
        context = {
            "username": userDetail["username"],
            "email": userDetail["email"],
            "videoObject":videoObject,
            "cartegories":cartegories,
            "allVideoDetails": allVideoDetails,
            "is_approved":is_approved,
            "latestVideos": latests,
            "greater": len(allVideoDetails) >= 5,
            "notifications":notice,
        }
    else:
         context = {
            "username": "username",
            "email": "email@gmail.com",
            "videoObject":videoObject,
            "cartegories":cartegories,
            "allVideoDetails": allVideoDetails,
            "latestVideos": latests,
            "greater": len(allVideoDetails) >= 5,
            "notifications":notice,
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
        videoQuality = []
        videoNumber = 0
        for vid in vidz:
            vid.quality = vid.quality.upper().strip()
            videoQuality.append(vid.quality.upper().strip())
            vidzUpdate.append(vid)
        for vidNUmber in vidz:
            # print(vidNUmber.quality, videoQuality[0])
            if vidNUmber.quality == videoQuality[0]:
                videoNumber += 1
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
        
        # DOwnloaded video
        downloaded = DownloadHistory.objects.filter(name = user["username"])
        downloadeds = []
        if downloaded.exists():
            for div in downloaded:
                downloadeds.append(div.video_name)
        onWatch = Onwatch.objects.filter(watcher = user["username"])
        if onWatch.exists():
            for div in onWatch:
                downloadeds.append(div.video_name)
                # print(div.video_name)
        # print(downloadeds)
        context = {
            "videoDetails":videoDetail,
            "video":vidzUpdate,
            "videolity": videolity[0],
            "user" :user,
            "cartExist": cartExist,
            "trending":popularVid,
            "buyer" : is_buyer,
            "downloaded": downloadeds,
            "videoNumber":videoNumber,
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
    messages = Message.objects.all().reverse()
    payments = DepositHistory.objects.all().reverse()
    download = DownloadHistory.objects.all().reverse()
    watch = Onwatch.objects.all().reverse()
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
        #print(uploadType)
        if uploadType == "video_details":
            form = VideoUploads(request.POST, request.FILES)
            if form.is_valid():
                
                form.save()
        elif uploadType == "video":
            #print("video")
            vidz = VideoForm(request.POST, request.FILES)
            if vidz.is_valid():
                print("valid")
                for fila in request.FILES.getlist('video'):
                    # Handle the uploaded file (e.g., save to storage)
                    #print(fila)
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
    user = userDetails(request)["userBuyrDetailsDi"]
    videos = Videos.objects.filter(name = str(request.GET["name"]).strip())
    playVideo = ''
    for vid in videos:
        playVideo = vid
        break
    videoCartegory = VideoUpload.objects.filter(cartegory = VideoUpload.objects.get(title = request.GET["name"]).cartegory)
    videoOther = []
    count = 0
    for videoCartegor in videoCartegory:
        if videoCartegor.title == request.GET["name"]:
            continue
        videoOther.append(videoCartegor)
        if count > 5:
            break
    
   
    context = {
        "playVideo":playVideo,
        "otherVideo":videoOther,
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
            Amount = int(request.POST["amount"])
            number = str(request.POST["phoneNumber"])
            phoneNumber = "254" + number[1:]
            # Your API username and password
            api_username = "0unBXb8nkf0BXLSUaWGz"
            api_password = "uuazzq2X33n4rFnKOh0Un5HMG8KrmU7TnJJYFxF3"
            # Concatenating username and password with colon
            credentials = f'{api_username}:{api_password}'
            # Base64 encode the credentials
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            # Creating the Basic Auth token
            basic_auth_token = f'Basic {encoded_credentials}'
            # Output the token
            # print(basic_auth_token)


            import requests

            url = 'https://backend.payhero.co.ke/api/v2/payments'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': basic_auth_token
            }
            print("sending data")
            data = {
                "amount": Amount,
                "phone_number": phoneNumber,
                "channel_id": 1238,
                "provider": "m-pesa",
                "external_reference": "INV-009",
                "callback_url": "https://kingstonemovies.xyz/stk/"
                # "callback_url":"https://smooth-vast-thrush.ngrok-free.app/stk/"
            }
            print("sending data....")
            response = requests.post(url, json=data, headers=headers).json()
            print(response)
            if response["success"]:
                depoExist = Payment.objects.filter(phone_number = phoneNumber)
                # delete list and add this new
                if depoExist.exists():
                    for dep in depoExist:
                        dep.delete()
                print("creting payments")
                Payment.objects.get_or_create(
                    username = user["username"],
                    phone_number = phoneNumber
                )
            else:
                return redirect("/deposit/")
            return redirect("/membership/dashboard/")
    else:
        is_buyer = False
    context = {
            "buyer":is_buyer
    }
    return render(request, "deposit.html",{"context": context} )

def download(request):
    if request.method == "POST":
        videoTitle = request.POST["videoTitle"].capitalize()
        quality = request.POST["quality"].capitalize()
        user = userDetails(request)["username"]
        # print(user)
        price = request.POST["price"]

        # Get movie with the name of videoTitle
        videozMatch = Videos.objects.filter(name = videoTitle)
        if videozMatch.exists():
            videoExist = True
            # get video details
            videozdetails = VideoUpload.objects.filter(title = videoTitle)
            videozdetail = ""
            for videozMa in videozdetails:
                    videozdetail = videozMa
                    break
            # video with Wanted pixel
            videoPixel = []
            for videozMa in videozMatch:
                if videozMa.quality.capitalize() == quality:
                    videoPixel.append(videozMa)
            print(videoPixel)
            # remove item from cart on download it the item exist in cart table
            existCart = Cart.objects.filter(video_name = videoTitle)
            if existCart.exists():
                existCart.delete()
            #check if downloaded:
            is_download = DownloadHistory.objects.filter(name = user)
            is_watch = Onwatch.objects.filter(watcher = user)
            paidList = []
            for isWatch in is_watch:
                paidList.append(isWatch.video_name)
            for isDownloaded in is_download:
                paidList.append(isDownloaded.video_name)
            # print(paidList)
            VideoPaid = False
            for payed in paidList:
                if payed == videoTitle:
                    VideoPaid = True
            if not VideoPaid:
                  # deduct payment from user Account
                userAccount = Buyers.objects.filter(username = user)
                if userAccount.exists():
                    for use in userAccount:
                        if int(use.account) >= int(price):
                            use.account = int(use.account) - int(price)
                            use.save()
                            # save download details to downloadhistory table
                            DownloadHistory.objects.create(
                                name = user,
                                video_name = videoTitle,
                                cost = price
                            )
                            break
                        else:
                          return redirect("/deposit/")
        else:
            videoExist = False
            videoPixel = False
            videozdetail = False
   # print(len(videoPixel))
    context = {
        "videos":videoPixel,
        "videoDetails":[videozdetail],
        "videoExist":videoExist
    }

    return render(request, "download.html", {"context":context})

@csrf_exempt
def stkCallback(request):
    print("paid done...")
    callback_data = json.loads(request.body)
    response = callback_data['response']
    if callback_data["status"]:
        print("status true and code added")
        Paymentcodes.objects.create(
            code = response['MpesaReceiptNumber'],
            amount = response["Amount"]
        )  
        try :
            paymentwaiting = Payment.objects.get(phone_number = response["Phone"])
            paymentExist = True
        except Payment.DoesNotExist:
            paymentExist = False

        if paymentExist:
            print("payment exist")
            userAccount = Buyers.objects.get(username = paymentwaiting.username)
            userAccount.account = int(userAccount.account) + response["Amount"]
            DepositHistory.objects.create(
                amount = response["Amount"],
                name = paymentwaiting.username
            )
            awaiting = AwaitingActivation.objects.filter(username = paymentwaiting.username)
            if awaiting.exists():
                print("awaiting found")
                for awyt in awaiting:
                    if userAccount.account  < int(awyt.price):
                        print("less balance")
                        awyt.delete()
                        # print("redirecting")
                        userAccount.save()
                        return redirect("/deposit/")
                    # print("deducting")
                    else:
                        print("more balance")
                        userAccount.account -= int(awyt.price)
                        # print("watching")
                        Onwatch.objects.create(
                            video_name = awyt.video_name,
                            watcher = awyt.username
                        )
                        awyt.delete()
                        userAccount.save()
            else:
                print("no waiting activation found")
                userAccount.save()
            paymentwaiting.delete() 
    # Return a success response to the M-Pesa server
    response_data = {'ResultStatus': True, 'ResultDesc': 'Success'}
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
    userCart = Cart.objects.filter(username = user).reverse()
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
        "all": len(Cart.objects.filter(username = user)) > 1,
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
        # print(request.POST["videoName"])
        videoDet = VideoUpload.objects.get(title = request.POST["videoName"])
        # print(videoDet.price,userAccount.account)
        if userAccount.account < videoDet.price:
            AwaitingActivation.objects.get_or_create(
                username = userDetails(request)["userBuyrDetailsDi"]["username"],
                video_name = request.POST["videoName"],
                price = VideoUpload.objects.get(title = request.POST["videoName"]).price
            )
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
# this is just a comment
def deactivate(request):
    if request.method == "POST":
        vide = Videos.objects.filter(video = request.POST["videoName"])
        vide.ended = True
        vide.save()
        print(request.POST["videoName"])
    return redirect("/membership/dashboard")
def search(request):
    searchTerm = request.GET["searchTerm"]
    videos = []
    videoDetail = VideoUpload.objects.all()
    for vids in videoDetail:
        if str(searchTerm).lower() in str(vids.title).lower():
            videos.append(vids)
    if len(videos) == 0:
        for vids in videoDetail:
            if str(searchTerm).lower() in str(vids.cartegory).lower():
                videos.append(vids)
    elif len(videos) == 0:
        for vids in videoDetail:
            if str(searchTerm).lower() in str(vids.typs).lower():
                videos.append(vids)
    # print(videoDetail.exists())
    context = {
        "videoDetail": videos,
        "searchTerm":str(searchTerm).capitalize(),
        
    }     
    return render(request, "search.html", {"context": context}) 
def cancelPurchase(request):
    videoName = request.POST["videoName"]
    videoExist = Onwatch.objects.filter(video_name = videoName)
    if videoExist.exists:
        for vids in videoExist:
            vids.delete()
    return redirect("/")

@login_required(login_url="/membership/login")
def downloadAll(request):
    if request.method == "POST":
        user = userDetails(request)["username"]
        allCarts = Cart.objects.filter(username = user)
        #check if downloaded:
        is_download = DownloadHistory.objects.filter(name = user)
        is_watch = Onwatch.objects.filter(watcher = user)
        paidList = set([])
        for isWatch in is_watch:
            paidList.add(isWatch.video_name)
        for isDownloaded in is_download:
            paidList.add(isDownloaded.video_name)
        
        # videos Title
        videoTitles = []
        videoTitlesNot = []
        for cart in allCarts:
            videoTitlesNot.append(cart.video_name)
            videoTitles.append(cart.video_name)
        # remove paid videos
        # print(videoTitlesNot)
        for paid in paidList:
            if paid in videoTitles:
                videoTitlesNot.remove(paid)
        # print(videoTitlesNot, "teo")
        # calculate total
        prize = 0
        for notPaid in videoTitlesNot:
            prize = prize + VideoUpload.objects.get(title = notPaid).price
        # print(prize)
        # deduct from account
        user = Buyers.objects.get(username = user)
        if user.account >= prize:
            user.account = user.account - prize
            user.save()
            # print(user.account)
            # add movies to downloaded
            for notpay in videoTitlesNot:
                DownloadHistory.objects.create(
                                name = user,
                                video_name = notpay,
                                cost =  VideoUpload.objects.get(title = notPaid).price
                            )
            # clear cart
            existCart = Cart.objects.filter(username = user)
            for cartz in existCart:
                if existCart.exists():
                    cartz.delete()
            # videos and video details
            videos = []
            videoDetails = []
            for vide in allCarts:
                videoDetails.append(VideoUpload.objects.get(title = vide.video_name))
                for vido in Videos.objects.filter(name = vide.video_name):
                    videos.append(vido)
        else:
            return redirect("/deposit/")
        context = {
            "videoExist": len(videos),
            "videoDetails": videoDetails,
            "videos": videos
        }
        return render(request, "download.html", {"context":context})
    else: 
        return redirect("/cart/")
        
