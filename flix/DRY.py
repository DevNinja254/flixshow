from Members.models import Buyers,Members

#return userdatiails on login

def userDetails(request):

    # pass request as a argument
    if request.user.is_authenticated:
        user = request.user

        # user information without username form Members table since authetication is based on email
        userDetailQuery = Members.objects.filter(email = user).values()
        userMembrID = 0
        userMembDetailsDic = ''

        # Assign Id from userDetails to userID
        for userdet in userDetailQuery:
            # user memeberId
            userMembDetailsDic = userdet
            userMembrID = userdet["id"]

        

        # Get username from buyer table, filtering by user iD frm members table
        userDetailQuery = Buyers.objects.filter(members_ptr_id = userMembrID).values()
        userBuyrDetailsDic = ''
        username = False
        # if user exist loop and assign username to username variable else let username be the email
        if userDetailQuery.exists():
            for usernam in userDetailQuery:
                userBuyrDetailsDic = usernam
                username = usernam["username"]
        userDetail = {
            "userMembDetailsDic": userMembDetailsDic,
            "userBuyrDetailsDi": userBuyrDetailsDic,
            "email": user,
            "username": str(username),
            "logged": True
        }
    else:
        userDetail = {
            "logged": False,
            
        }
           

    return userDetail        
        
        

        
