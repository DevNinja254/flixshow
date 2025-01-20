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
    # print(endFalse, endTrue)
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
    # Downloaded movies
    downloaded = DownloadHistory.objects.filter(name = user["username"])
    if downloaded.exists():
        for div in downloaded:
            titles.append(div.video_name)
        # print(downloadeds)
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
            print(basic_auth_token)


            import requests

            url = 'https://backend.payhero.co.ke/api/v2/payments'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': basic_auth_token
            }
            data = {
                "amount": Amount,
                "phone_number": phoneNumber,
                "channel_id": 1238,
                "provider": "m-pesa",
                "external_reference": "INV-009",
                "callback_url": "https://kingstonemovies.xyz/stk/"
            }

            response = requests.post(url, json=data, headers=headers)
            # print(response.json())
            paymentDict = {

            }
            for key in response.json():
                paymentDict[key] = response.json()[key]
            
            print(paymentDict['success'])
            # insert pending info
            if paymentDict['success']:
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
    callback_data = json.loads(request.body)
    print(callback_data)
     # Check the result code
    amount = None
    phone_number = None
    result_status = callback_data['response']['Status']
    if result_status == "Success":
        amount = callback_data['response']['Amount']
        phone_number=callback_data['response']['Phone']
    
    
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
    # Return a success response to the M-Pesa server
    response_data = {'ResultStatus': result_status, 'ResultDesc': 'Success'}
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
        # print(videoDet.price,userAccount.account)
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
    videoDetail = VideoUpload.objects.filter(title = searchTerm.capitalize())
    if videoDetail.exists() ==False:
       videoDetail = VideoUpload.objects.filter(cartegory = searchTerm.capitalize())
    elif videoDetail.exists() ==False:
        videoDetail = VideoUpload.objects.filter(typs = searchTerm.capitalize())
    # print(videoDetail.exists())
    context = {
        "videoDetail": videoDetail,
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
    user = userDetails(request)["username"]
    total= 0
    videoNotExist = []
    videoExist = []
    allCarts = Cart.objects.filter(username = user)
    downloadQuality = ""
     #check if downloaded:
    is_download = DownloadHistory.objects.filter(name = user)
    is_watch = Onwatch.objects.filter(watcher = user)
    paidList = []
    videodetails = set([])
    videoDetailz = []
    for isWatch in is_watch:
        paidList.append(isWatch.video_name)
    for isDownloaded in is_download:
        paidList.append(isDownloaded.video_name)
    # print(paidList)
    for cart in allCarts:
        videoUploaded = Videos.objects.filter(name = cart.video_name)
        if videoUploaded.exists():
            for vid in videoUploaded:
                quality = str(VideoUpload.objects.get(title = vid.name).Quality).strip().split(" ")[0]
                if str(vid.quality) == str(quality):
                    videoExist.append(vid)
                    videodetails.add(vid.name)
        else:
            videoNotExist.append(cart.video_name)
    # for paid in paidList:
    #             if str(cart.video_name) != str(paid): 
    #                 price = int(VideoUpload.objects.get(title = cart.video_name).price)
                    # total += price
    for vidd in videodetails:
        videoDetailz.append(VideoUpload.objects.get(title = vidd))
        if DownloadHistory.objects.filter(video_name = vidd).exists():
            pass
            # total += int(VideoUpload.objects.get(title = vidd).price)
        elif Onwatch.objects.filter(video_name = vidd).exists():
            # print("exist1")
            pass
            # total += int(VideoUpload.objects.get(title = vidd).price)
        else:
            total += int(VideoUpload.objects.get(title = vidd).price)
        cartName = Cart.objects.get(video_name = vidd)
        cartName.delete()
    print(total)
    if total > 0 :
        userAccount = Buyers.objects.get(username = user)
        if int(userAccount.account) >= total:
            userAccount.account = int(userAccount.account) - total
            userAccount.save()
            for vidDown in videoExist:
                for paid in paidList:
                    if str(paid) != vidDown.name:
                        DownloadHistory.objects.create(
                                name = user,
                                video_name = vidDown.name,
                                cost = VideoUpload.objects.get(title = vidDown.name).price  
                            )
   
                    # deleteCart = Cart.objects.get(video_name = paid)
                    # deleteCart.delete()
        else:
            return redirect("/deposit/")
    print(1, videoExist)
    # print(paidList)
    context = {
        "videos":videoExist,
        "videoDetails":videoDetailz,
        "videoExist":len(videoNotExist) == 0
    }

    return render(request, "download.html", {"context":context})
