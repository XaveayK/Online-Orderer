cd C:\Users\kidston\Desktop\scraping\dist
SetLocal EnableDelayedExpansion

@echo off 

set YES="y"

IF EXIST userInfo.txt (
    set /p CHANGEUSER="Would you like to update user info (y/n)? "
    if !CHANGEUSER! == !YES! (
        DEL userInfo.txt
        CALL:GETUSERINFO
    )
) else (
    CALL:GETUSERINFO
)

IF EXIST credInfo.txt (
    set /p CHANGECRED="Would you like to update credit card info (y/n)? "
    if !CHANGECRED! == !YES! (
        DEL credInfo.txt
        CALL:GETCREDITINFO
    )
) ELSE (
    CALL:GETCREDITINFO
)

IF EXIST twilioCred.txt (
    set /p CHANGTWI="Would you like to update Twilio information (y/n)? "
    if !CHANGETWI! == !YES! (
        DEL twilioCred.txt
        CALL:GETTWILIOINFO
    )
) ELSE (
    CALL:GETTWILIOINFO
) 

:loop
start "benchOrder" ord.exe https://www.bellsofsteel.com/product/flat-incline-decline-bench/ 
start "rackOrder" ord.exe https://www.bellsofsteel.com/product/commercial-power-rack-light/
timeout /t 1500 >null
taskkill /f /im chrome.exe >nul
taskkill /f /im ord.exe >nul
taskkill /f /im chromedriver.exe >nul
timeout /t 3 >null
goto loop

:GETTWILIOINFO
    set /p TWIACC="Account SID Twilio: "
    set /p TWIAUTH="Twilio authentication token: "
    set /p TWIPHONE="Twilio Phone Number: "
    echo %TWIACC%>%cd%\twilioCred.txt
    echo %TWIAUTH%>%cd%\twilioCred.txt
    echo %TWIPHONE%>%cd%\twilioCred.txt
EXIT /B 0

:GETCREDITINFO
    set /p CCNUM="Credit Card Number: "
    set /p SECNUM="Security Number: "
    set /p EXPIRY="Card Expiry Date (mmyy): "
    ECHO %CCNUM%>%cd%\credInfo.txt
    ECHO %SECNUM%>%cd%\credInfo.txt
    ECHO %EXPIRY%>%cd%\credInfo.txt
EXIT /B 0

:GETUSERINFO
    set /p TEXTNUM="Phone Number: "
    set /p FNAME="First Name: "
    set /p LNAME="Last Name: "
    set /p ADDRESS="Address: "
    set /p POSTAL="Postal Code: "
    set /p PROV="Province: "
    set /p CITY="City: "
    set /p EMAIL="Email: "
    ECHO %TEXTNUM%>%cd%\userInfo.txt
    ECHO %FNAME%>%cd%\userInfo.txt
    ECHO %LNAME%>%cd%\userInfo.txt
    ECHO %ADDRESS%>%cd%\userInfo.txt
    ECHO %POSTAL%>%cd%\userInfo.txt
    ECHO %PROV%>%cd%\userInfo.txt
    ECHO %CITY%>%cd%\userInfo.txt
    ECHO %EMAIL%>%cd%\userInfo.txt
EXIT /B 0