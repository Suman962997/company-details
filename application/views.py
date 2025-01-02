from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import serializersclass
from .models import Company
import requests
from bs4 import BeautifulSoup
import re
from rest_framework.parsers import MultiPartParser, FormParser
import os
from PyPDF2 import PdfReader


class webscraping(APIView):
    parser_classes=(MultiPartParser,FormParser)

    def post(self,request,*args,**kwargs):       
        url = request.data.get('url') 
        file = request.data.get('file')
        # file = request.FILES.get('file')
        print(file)

        if url:
            request=requests.get(url)
            souptext=BeautifulSoup(request.text,'html.parser').text
            soup=BeautifulSoup(request.text,'html.parser')        
            # print(soup)
            # print(souptext)
            print('It is url')

            def companynamefun():

                            #company name
                title = soup.find('title')
                if title:
                    company_name = title.text.strip()  
                    print('33  if working ',company_name )

                else:
                    print('35  else working')
                    meta_author = soup.find('meta', attrs={'name': 'author'})
                    if meta_author and meta_author.get('content'):
                        company_name = meta_author['content']
                    else:
                        company_name = "Company name not found"

                words_to_remove = ['contact', 'CONTACT', 'Contact','Us','-',':','|']
                for word in words_to_remove:
                    company_name = company_name.replace(word, '')

                print(f'46 company name is',company_name)
                if company_name:
                    print(company_name)
                    return company_name
                else:
                    print()
                    return company_name
            companynamefun()

            
            def addressfun():
                                        #ADDRESS  
            #################################################

                pincode_pattern = r'\b\d{3}\s?\d{3}\b'
                door_num_pattern=r'\b(?:[Aa]ddress|[Ss]t|[Nn]o|[Dd]oor[Ff]loor|[Ss]alai|[Bb]lock|[Pp]lot|[Ss]treet|[Nn]agar)\b'
                street_pattern = r'\b(?:[Ss]treet|[Nn]agar|[Ff]loor|[Rr]oad|[Ss]t|[Aa]venue|[Ll]ane|[Ii]ndia|[Cc]ennai|[Bb]oulevard|[Ww]ay|[Dd]rive|[Tt]amil|[Tt]errace)\b'
                tamil_nadu_districts_pattern = r'\b(?:Ariyalur|Chengalpattu|Chennai|Coimbatore|Cuddalore|Dharmapuri|Dindigul|Erode|Kallakurichi|Kanchipuram|Kanyakumari|Karur|Krishnagiri|Madurai|Mayiladuthurai|Nagapattinam|Namakkal|Nilgiris|Perambalur|Pudukkottai|Ramanathapuram|Ranipet|Salem|Sivagangai|Tenkasi|Thanjavur|Theni|Thoothukudi|Tiruchirappalli|Tirunelveli|Tirupattur|Tiruppur|Tiruvallur|Tiruvannamalai|Tiruvarur|Vellore|Villupuram|Virudhunagar)\b'
                indian_states_pattern = r'\b(?:Andhra Pradesh|Bengaluru|Arunachal Pradesh|Assam|Bihar|Chhattisgarh|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|Andaman and Nicobar Islands|Chandigarh|Dadra and Nagar Haveli and Daman and Diu|Delhi|Jammu and Kashmir|Ladakh|Lakshadweep|Puducherry)\b'
                country_pattern = r'\b(?:Afghanistan|Albania|Algeria|Andorra|Angola|Antigua and Barbuda|Argentina|Armenia|Australia|Austria|Azerbaijan|Bahamas|Bahrain|Bangladesh|Barbados|Belarus|Belgium|Belize|Benin|Bhutan|Bolivia|Bosnia and Herzegovina|Botswana|Brazil|Brunei|Bulgaria|Burkina Faso|Burundi|Cabo Verde|Cambodia|Cameroon|Canada|Central African Republic|Chad|Chile|China|Colombia|Comoros|Congo \(Congo-Brazzaville\)|Costa Rica|Croatia|Cuba|Cyprus|Czechia \(Czech Republic\)|Denmark|Djibouti|Dominica|Dominican Republic|Ecuador|Egypt|El Salvador|Equatorial Guinea|Eritrea|Estonia|Eswatini \(fmr\. \'Swaziland\'\)|Ethiopia|Fiji|Finland|France|Gabon|Gambia|Georgia|Germany|Ghana|Greece|Grenada|Guatemala|Guinea|Guinea-Bissau|Guyana|Haiti|Holy See|Honduras|Hungary|Iceland|India|Indonesia|Iran|Iraq|Ireland|Israel|Italy|Jamaica|Japan|Jordan|Kazakhstan|Kenya|Kiribati|Korea \(North\)|Korea \(South\)|Kuwait|Kyrgyzstan|Laos|Latvia|Lebanon|Lesotho|Liberia|Libya|Liechtenstein|Lithuania|Luxembourg|Madagascar|Malawi|Malaysia|Maldives|Mali|Malta|Marshall Islands|Mauritania|Mauritius|Mexico|Micronesia|Moldova|Monaco|Mongolia|Montenegro|Morocco|Mozambique|Myanmar \(formerly Burma\)|Namibia|Nauru|Nepal|Netherlands|New Zealand|Nicaragua|Niger|Nigeria|North Macedonia|Norway|Oman|Pakistan|Palau|Palestine State|Panama|Papua New Guinea|Paraguay|Peru|Philippines|Poland|Portugal|Qatar|Romania|Russia|Rwanda|Saint Kitts and Nevis|Saint Lucia|Saint Vincent and the Grenadines|Samoa|San Marino|Sao Tome and Principe|Saudi Arabia|Senegal|Serbia|Seychelles|Sierra Leone|Singapore|Slovakia|Slovenia|Solomon Islands|Somalia|South Africa|South Sudan|Spain|Sri Lanka|Sudan|Suriname|Sweden|Switzerland|Syria|Tajikistan|Tanzania|Thailand|Timor-Leste|Togo|Tonga|Trinidad and Tobago|Tunisia|Turkey|Turkmenistan|Tuvalu|Uganda|Ukraine|United Arab Emirates|United Kingdom|United States of America|Uruguay|Uzbekistan|Vanuatu|Venezuela|Vietnam|Yemen|Zambia|Zimbabwe)\b'


                address_element=[]

                address_text=[]
                for element in soup.find_all(True):
                    if element.name in ['script', 'style']:
                        continue
                    # Combine text content of the element
                    text = element.get_text(strip=True)
                    # Check if both patterns are present in the text
                    if re.search(pincode_pattern, text) and re.search(street_pattern, text,re.IGNORECASE):
                        address_element.append(element.name)
                        # print('hihih',text)
                        address_text.append(text)                                
                        print('78 ')

                if not address_text:    
                    for element in soup.find_all(True):
                        if element.name in ['script', 'style']:
                            continue
                        # Combine text content of the element
                        text = element.get_text(strip=True)
                        # Check if both patterns are present in the text
                        if re.search(pincode_pattern, text) and re.search(street_pattern, text,re.IGNORECASE) or re.search(indian_states_pattern, text,re.IGNORECASE): #and re.search(country_pattern, text,re.IGNORECASE):
                            address_element.append(element.name)
                            # print('serao',text)
                            address_text.append(text)                                
                            print('91')  

         
                if not address_text :    
                    for element in soup.find_all(True):
                        if element.name in ['script', 'style']:
                            continue
                        # Combine text content of the element
                        text = element.get_text(strip=True)
                        # Check if both patterns are present in the text
                        if re.search(pincode_pattern, text) and re.search(door_num_pattern, text,re.IGNORECASE) or re.search(street_pattern, text,re.IGNORECASE)or re.search(tamil_nadu_districts_pattern, text,re.IGNORECASE) or re.search(country_pattern, text,re.IGNORECASE): #or re.search(country_pattern, text,re.IGNORECASE):
                            address_element.append(element.name)
                            address_text.append(text)                                
                            print('103')




                if not address_text:
                    address="ADDRESS not found!"
                    print('98',address)
                    return address

                if (len(address_text)>0):
                    # print(f'All address{address_text}')
                    address=address_text[-1]
                    print('101 company address',address)
                    return address

                else:
                    address=address_text
                    print('104 company address',address)
                    return address        

            addressfun()


            def contactfun():
            #################################################
                            #CONTACT NUMBER        
                phone_pattern = re.compile(r'\+?\d[\d\s().-]{7,}\d')        
                phone_numbers = phone_pattern.findall(souptext)
                contactnumber = [re.sub(r'[^\d+]', '', number) for number in phone_numbers]
                contact = []
                contactarr=[]

                country_calling_codes = [
                    "+93", "+355", "+213", "+1-684", "+376", "+244", "+1-264", "+672", "+1-268", "+54", "+374",
                    "+297", "+61", "+43", "+994", "+1-242", "+973", "+880", "+1-246", "+375", "+32", "+501", "+229",
                    "+1-441", "+975", "+591", "+387", "+267", "+55", "+246", "+673", "+359", "+226", "+257", "+855",
                    "+237", "+1", "+238", "+1-345", "+236", "+235", "+56", "+86", "+57", "+269", "+243", "+242",
                    "+506", "+225", "+385", "+53", "+357", "+420", "+45", "+253", "+1-767", "+1-809", "+593", "+20",
                    "+503", "+240", "+291", "+372", "+251", "+679", "+358", "+33", "+241", "+220", "+995", "+49",
                    "+233", "+30", "+1-473", "+1-671", "+502", "+224", "+245", "+592", "+509", "+504", "+852", "+36",
                    "+354", "+91", "+62", "+98", "+964", "+353", "+972", "+39", "+1-876", "+81", "+962", "+7", "+254",
                    "+686", "+850", "+82", "+965", "+996", "+856", "+371", "+961", "+266", "+231", "+218", "+423",
                    "+370", "+352", "+853", "+389", "+261", "+265", "+60", "+960", "+223", "+356", "+692", "+596",
                    "+222", "+230", "+52", "+691", "+373", "+377", "+976", "+382", "+1-664", "+212", "+258", "+95",
                    "+264", "+674", "+977", "+31", "+687", "+64", "+505", "+227", "+234", "+683", "+672", "+47",
                    "+968", "+92", "+680", "+970", "+507", "+675", "+595", "+51", "+63", "+48", "+351", "+1-787",
                    "+974", "+40", "+7", "+250", "+1-869", "+1-758", "+1-784", "+685", "+378", "+239", "+966", "+221",
                    "+381", "+248", "+232", "+65", "+421", "+386", "+677", "+252", "+27", "+34", "+94", "+249", "+597",
                    "+46", "+41", "+963", "+886", "+992", "+255", "+66", "+670", "+228", "+676", "+1-868", "+216",
                    "+90", "+993", "+688", "+256", "+380", "+971", "+44", "+1", "+598", "+998", "+678", "+58", "+84",
                    "+967", "+260", "+263"
                ]

                for i in contactnumber:
                    print('85')
                    if any(i.startswith(code) for code in country_calling_codes):
                        contact.append(i)
                if not contact and contact:
                    print('90')
                    pattern = r'\+?\d[\d\s\-\.\(\)]{8,}\d'
                    phone_numbers = re.findall(pattern, souptext)
                    contact.append(phone_numbers)
                if not contact and contact:
                    print('96')
                    pattern = r'\b(?:\d[- ]?){9}\d\b|\b(?:\d[- ]?){11}\d\b'
                    phone_numbers=re.findall(pattern,souptext )
                    contact.append(phone_numbers)
                if not contact and contact:
                    print('98')
                    pattern = r'\b\d{3} \d{4} \d{4}\b'
                    phone_numbers = re.findall(pattern, souptext)
                    contact.append(phone_numbers)

                if not contact:
                    contact.append("contactnumber not found!")
                    print('seted')  


                for i in contact:
                    if (len(i)>8):
                        contactarr.append(i)
                contact_number=set(contactarr)
                print(contact_number)
                return contact_number
            contactfun()


            def gmailfun():
                                    #GMAIL ID            
                if (1==1):                       
                    emails = []
                    tlds = [
                        ".com", ".org", ".net", ".info", ".biz", ".name", ".pro", ".edu", ".gov", ".mil", ".int",
                        ".us", ".uk", ".in", ".au", ".ca", ".de", ".fr", ".jp", ".cn", ".br", ".ru", ".za", ".nz",
                        ".sg", ".hk", ".ie", ".it", ".es", ".mx", ".kr", ".id", ".ph", ".tr", ".ar", ".ng", ".ke",    
                        ".xyz", ".top", ".online", ".site", ".club", ".store", ".tech", ".website", ".space", ".me",
                        ".io", ".app", ".dev", ".art", ".design", ".blog", ".news", ".cloud", ".guru", ".life", ".money",
                        ".solutions", ".world", ".email", ".shop", ".love", ".team", ".fun", ".agency",    
                        ".travel", ".museum", ".aero", ".coop", ".jobs", ".mobi", ".tel", ".post", ".asia", ".cat",    
                        ".рф", ".中国", ".भारत", ".السعودية", ".한국", ".ไทย", ".рб", ".இலங்கை", ".شبكة",    
                        ".tv", ".fm", ".io", ".ai", ".ly"]


                    for mailto in soup.select('a[href^=mailto]'):
                        print('121')
                        matches=mailto['href'].replace('mailto:', '').strip().replace('[','').replace(']','')
                        emails.append(matches)
                        print('197 emails ',emails)
                    if not emails or emails:
                        print('127')
                        matches=re.findall( r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',souptext,re.IGNORECASE)
                        emails.append(matches)
                    if not emails or emails:
                        print('130')
                        matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+',souptext,re.IGNORECASE)         
                        emails.append(matches)
                    if not emails or emails:
                        print('136')
                        matches = re.findall( r'\b[A-Za-z0-9._%+-]+@gmail\.com\b',souptext,re.IGNORECASE)         
                        emails.append(matches)
                    

                    if not emails or emails:
                        print('136')
                        matches = re.findall( r'\b\w*@\w*\b',souptext,re.IGNORECASE)         
                        emails.append(matches)

                        print('211 it is match',matches)


                    
                    if not emails or emails:
                        print('163')
                        tld_pattern = '|'.join(re.escape(tld) for tld in tlds)
                        email_regex = rf'\b\w+@\w+(?:\.\w+)*(?:{tld_pattern})\b'
                        matches = re.findall(email_regex,souptext)         
                        emails.append(matches)

                        
                    # if not emails:
                    #     emails=None
                    #     print('Email not exist !')
                    #     return emails


                    flattened_emails = []
                    if emails:                    
                        for item in emails :
                            if isinstance(item, list):
                                flattened_emails.extend(item)
                            else:
                                flattened_emails.append(item)

                    print('224 emails  ',flattened_emails)



                    if not flattened_emails:
                        print('222  NOT EMAIL EXIST')
                        return None

                    if flattened_emails:    
                        emails=set(flattened_emails)
                        print(f'company mail is [{emails}]')
                        print('999')
                        return emails
                    


            gmailfun()
            def websitefun():
                website=url
                return website

            gmailfunstr=str(gmailfun())

                                            # WEBSITE

            def upcompanyfun():
                if gmailfun() and websitefun():
                    companyname = ''
                    def find_common(string1,string2):
                        print('%$%#@ CHECKER @#@!$')
                        string1_list=str(string1).split(" ")
                        result=""
                        for item in string1_list:
                            matcher_obj=re.search(item,string2,re.IGNORECASE)
                            if matcher_obj is not None:
                                result+=string2[matcher_obj.start():matcher_obj.end()]+" "
                                print('219',result)
                            if matcher_obj is None:
                                print('220 IT IS NONE ')
                                companyname=companynamefun().split()
                                print('302',companyname)
                                do=[]
                                website285=str(websitefun())
                                print('304',website285)
                                for sdr in companyname:
                                    print('305',sdr)
                                    d=re.search(sdr.strip(),website285,re.IGNORECASE)
                                    print('307',d)
                                    if d is not None:
                                        do.append(website285[d.start():d.end()])

                                if None is do or not do:
                                    print('NONE NENE NONE NONE',do)
                                    return companyname
                                print('289',do)
                                if do:
                                    print('do is',do)
                                    do =str(do)
                                    return do
                        result= re.sub(r'\b(?:com|in|org|net|contact|contact-us|us)\b', ' ',result,re.IGNORECASE)      
                        print(f'result is {result,type(result)},')
                        return result          
                    listemails=str(gmailfunstr).replace("@"," ").replace("."," ").replace('{',' ').replace('}',' ')
                    # print('230',s)
                    company=(find_common(listemails.strip(),websitefun()))
                    splitcom=company
                    print('212',splitcom)
                    companyname=str(splitcom).strip().replace(',','')
                    return companyname


                if not gmailfun() and websitefun() and companynamefun():
                    print('268 ',websitefun(),companynamefun())

                    companyname = ''
                    def find_common2(string1,string2):
                        print('272 !!!)!))!)!')
                        string1_list=str(string1).split(" ")
                        result=""
                        for item in string1_list:
                            print(item)
                            matcher_obj=re.search(item,string2,re.IGNORECASE)
                            if matcher_obj is not None:
                                result+=string2[matcher_obj.start():matcher_obj.end()]+" "
                                print('280',result)
                            if matcher_obj is None:

                                companyname=companynamefun().split()
                                do=[]
                                website285=websitefun()
                                for sdr in companyname:
                                    print('352',sdr)
                                    d=re.search(sdr.strip(),website285,re.IGNORECASE)
                                    print('355',d)
                                    if d is not None:
                                        do.append(website285[d.start():d.end()])
                                if None is do or not do:
                                    print('NONE NENE NONE NONE',do)
                                    return companyname
                                print('289',do)
                                if do:
                                    print('do is',do)
                                    do =str(do).strip()
                                    return do

                        result= re.sub(r'\b(?:com|in|org|net|contact|contact-us)\b', ' ',result,re.IGNORECASE)      
                        print(f'result is {result,type(result)},')
                        return result          
                    # print('230',s)
                    company=(find_common2(companynamefun().strip(),websitefun()))
                    print('359',company)
                    splitcom=company
                    print('289',splitcom)
                    companyname=str(splitcom).strip().replace(',','')
                    return companyname




                if  not gmailfun() and not websitefun() and companynamefun():
                    print('273 ',companynamefun() )
                    return companynamefun()


                upcompanyfun()



                    # SAVE
            


            print('********************************',type(upcompanyfun),upcompanyfun(),'******',type(addressfun()),addressfun(),'******',type(contactfun()),contactfun(),'******',type(gmailfun()),gmailfun(),'*****',type(websitefun()),websitefun(),'*******************************')

            data = {
            "company_name":str(upcompanyfun()),
            "address":str(addressfun()),
            "contact_number":str(contactfun()),
            "email":str( gmailfun()),
            "website":str( websitefun()),
            }
            serializer=serializersclass(data=data)
            if serializer.is_valid():
                serializer.save()
                print('saved')
            else:
                print('NOT SAVE')

                        #FILE#
#


        if file:
            reader = PdfReader(file)
            filetext = ""
            for page in reader.pages:
                filetext += page.extract_text() 
            print('It is file',filetext)

                    #COMPANY NAME
            def companynametext():
                find_words=['technology','solutions','tech','corprations','infotech',' services','soft','Pvt Ltd',' Enterprises','company','web','web design','digital']
                companies=[]
                for i in find_words:# or  Find_words or FIND_WORDs:
                    company_pattern=r'\b(\w+)\s+'+re.escape(i)
                    companies+=re.findall(company_pattern,filetext,re.IGNORECASE)

                print(f'It is comapanies : {type(companies)},{companies}')
                if companies:
                    return companies

                else:
                    print(companies)
                    return companies
            # companynametext()


            def addresstext():
                print('address')
                                
                    #ADDRESS
                pincode_pattern = r"\b\d{3}\s?\d{3}\b"
                street_pattern = r'\b(?:[Aa]ddress|[Ff]loor|[Ss]treet|[Ss]alai|[Pp]lot|[Bb]lock|[Nn]agar|[Rr]oad|[Rr]d|[Aa]venue|[Ll]ane|[Bb]oulevard|[Ww]ay|[Dd]rive|[Tt]amil|[Tt]errace)\b'
                door_num_pattern=r'\b(?:[Aa]ddress|[Ss]t|[Nn]o|[Dd]oor[Ff]loor|[Ss]alai|[Bb]lock|[Pp]lot|[Ss]treet|[Nn]agar)\b'
                country_pattern = r'\b(?:Afghanistan|Albania|Algeria|Andorra|Angola|Antigua and Barbuda|Argentina|Armenia|Australia|Austria|Azerbaijan|Bahamas|Bahrain|Bangladesh|Barbados|Belarus|Belgium|Belize|Benin|Bhutan|Bolivia|Bosnia and Herzegovina|Botswana|Brazil|Brunei|Bulgaria|Burkina Faso|Burundi|Cabo Verde|Cambodia|Cameroon|Canada|Central African Republic|Chad|Chile|China|Colombia|Comoros|Congo \(Congo-Brazzaville\)|Costa Rica|Croatia|Cuba|Cyprus|Czechia \(Czech Republic\)|Denmark|Djibouti|Dominica|Dominican Republic|Ecuador|Egypt|El Salvador|Equatorial Guinea|Eritrea|Estonia|Eswatini \(fmr\. \'Swaziland\'\)|Ethiopia|Fiji|Finland|France|Gabon|Gambia|Georgia|Germany|Ghana|Greece|Grenada|Guatemala|Guinea|Guinea-Bissau|Guyana|Haiti|Holy See|Honduras|Hungary|Iceland|India|Indonesia|Iran|Iraq|Ireland|Israel|Italy|Jamaica|Japan|Jordan|Kazakhstan|Kenya|Kiribati|Korea \(North\)|Korea \(South\)|Kuwait|Kyrgyzstan|Laos|Latvia|Lebanon|Lesotho|Liberia|Libya|Liechtenstein|Lithuania|Luxembourg|Madagascar|Malawi|Malaysia|Maldives|Mali|Malta|Marshall Islands|Mauritania|Mauritius|Mexico|Micronesia|Moldova|Monaco|Mongolia|Montenegro|Morocco|Mozambique|Myanmar \(formerly Burma\)|Namibia|Nauru|Nepal|Netherlands|New Zealand|Nicaragua|Niger|Nigeria|North Macedonia|Norway|Oman|Pakistan|Palau|Palestine State|Panama|Papua New Guinea|Paraguay|Peru|Philippines|Poland|Portugal|Qatar|Romania|Russia|Rwanda|Saint Kitts and Nevis|Saint Lucia|Saint Vincent and the Grenadines|Samoa|San Marino|Sao Tome and Principe|Saudi Arabia|Senegal|Serbia|Seychelles|Sierra Leone|Singapore|Slovakia|Slovenia|Solomon Islands|Somalia|South Africa|South Sudan|Spain|Sri Lanka|Sudan|Suriname|Sweden|Switzerland|Syria|Tajikistan|Tanzania|Thailand|Timor-Leste|Togo|Tonga|Trinidad and Tobago|Tunisia|Turkey|Turkmenistan|Tuvalu|Uganda|Ukraine|United Arab Emirates|United Kingdom|United States of America|Uruguay|Uzbekistan|Vanuatu|Venezuela|Vietnam|Yemen|Zambia|Zimbabwe)\b'
                indian_states_pattern = r'\b(?:Andhra Pradesh|Bengaluru|Arunachal Pradesh|Assam|Bihar|Chhattisgarh|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|Andaman and Nicobar Islands|Chandigarh|Dadra and Nagar Haveli and Daman and Diu|Delhi|Jammu and Kashmir|Ladakh|Lakshadweep|Puducherry)\b'
                tamil_nadu_districts_pattern = r'\b(?:Ariyalur|Chengalpattu|Chennai|Coimbatore|Cuddalore|Dharmapuri|Dindigul|Erode|Kallakurichi|Kanchipuram|Kanyakumari|Karur|Krishnagiri|Madurai|Mayiladuthurai|Nagapattinam|Namakkal|Nilgiris|Perambalur|Pudukkottai|Ramanathapuram|Ranipet|Salem|Sivagangai|Tenkasi|Thanjavur|Theni|Thoothukudi|Tiruchirappalli|Tirunelveli|Tirupattur|Tiruppur|Tiruvallur|Tiruvannamalai|Tiruvarur|Vellore|Villupuram|Virudhunagar)\b'
                address=[]

                if re.findall(street_pattern, filetext,re.IGNORECASE):

                    matches = re.findall(street_pattern, filetext,re.IGNORECASE)
                    print('fcgvjhbjnk',matches)

                    lines = filetext.split('\n')
                    for line in lines:
                        if re.search(street_pattern, line, re.IGNORECASE):
                            address.append(line)
                    print('465',address)


                    # return result

                    # return result
                if re.findall(tamil_nadu_districts_pattern, filetext,re.IGNORECASE):

                    matches = re.findall(tamil_nadu_districts_pattern, filetext,re.IGNORECASE)
                    print('uyhsdjk',matches)
                    result = []

                    lines = filetext.split('\n')
                    for line in lines:
                        # If there is a match in the line, store it
                        if re.search(tamil_nadu_districts_pattern, line, re.IGNORECASE):
                            address.append(line)
                    print('492',address)
                    # return result



                if re.findall(country_pattern, filetext,re.IGNORECASE):

                    matches = re.findall(country_pattern, filetext,re.IGNORECASE)
                    print('yuynas',matches)
                    result = []

                    lines = filetext.split('\n')
                    for line in lines:
                        # If there is a match in the line, store it
                        if re.search(country_pattern, line, re.IGNORECASE):
                            address.append(line)
                    print('495',address)
                    # return result


                if re.findall(indian_states_pattern, filetext,re.IGNORECASE):

                    matches = re.findall(indian_states_pattern, filetext,re.IGNORECASE)
                    print('502',matches)
                    result = []

                    lines = filetext.split('\n')
                    for line in lines:
                        # If there is a match in the line, store it
                        if re.search(indian_states_pattern, line, re.IGNORECASE):
                            address.append(line)
                    print('465',address)
                
            
                if re.findall(pincode_pattern, filetext,re.IGNORECASE):

                    matches = re.findall(pincode_pattern, filetext,re.IGNORECASE)
                    print('ygynd',matches)
                    result = []

                    lines = filetext.split('\n')
                    for line in lines:
                        # If there is a match in the line, store it
                        if re.search(pincode_pattern, line, re.IGNORECASE):
                            address.append(line)
                    print('481',address)



                if not address:
                    address=''
                print(f'It is address : {address}')
                if address:
                    address=set(address)
                    return address                

            # addresstext()

            def contacttext():

                    # CONTACT NUMBER

                phone_pattern = re.compile(r'\+?\d[\d\s().-]{7,}\d')        
                phone_numbers = phone_pattern.findall(filetext)
                contactnumber = [re.sub(r'[^\d+]', '', number) for number in phone_numbers]
                contact = []
                valid_country_codes = {"+90", "+91", "99","+61", "+81", "+85", "+86",'044-','04'}
                for i in contactnumber:
                    print('85')
                    if any(i.startswith(code) for code in valid_country_codes):
                        contact.append(i)
                contact_number=set(contact)

                if not contact_number:

                    phone_pattern = r'\b\d{10}\b'
                    phone_numbers=re.findall(phone_pattern,filetext)
                    contact_number=str(phone_numbers)
                    print('294')

                if not contact_number:
                    pattern = r'\+?\d[\d\s\-\.\(\)]{8,}\d'
                    phone_numbers = re.findall(pattern, souptext)
                    print('299')
                    contact=phone_numbers

                if not contact_number:
                    pattern = r'\b(?:\d[- ]?){9}\d\b|\b(?:\d[- ]?){11}\d\b'
                    phone_numbers=re.findall(pattern,souptext )
                    print('305')
                    contact=phone_numbers            
                if not contact_number:
                    pattern = r'\b\d{3} \d{4} \d{4}\b'
                    phone_numbers = re.findall(pattern, souptext)
                    print('310')
                    contact=phone_numbers

                if not contact_number:
                    phone_pattern= r"^\+\d{10,15}$"
                    phone_numbers=re.findall(phone_pattern,filetext)
                    print('301')
                    contact_number=set(phone_numbers)
                

                if contact_number:
                    return set(contact_number)

                if not contact_number:
                    contact_number=''
                    return contact_number
                print(f'It is contact : {contact_number}')



                # return contact_number

            # contacttext()
            
            def mailtext():
                                #     #MAIL ID

                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                email_id=re.findall(email_pattern,filetext,re.IGNORECASE)

                if not email_id:
                    company_mailid=''
                    print(f'It is comapny mailid : {company_mailid}')
                    return company_mailid 

                    
                if email_id:
                    print(f'It is comapny mailid : {email_id}')
                    company_mailid=set(email_id)
                    return company_mailid
            
            # mailtext()
            
            def websitefuntext():
                    #COMAPNY WEBSITE

                website_pattern = r'\b(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b'
                website=re.findall(website_pattern,filetext,re.IGNORECASE)

                if not website:
                    website=''
                    print('website is not found 406')
                    return website

                if website:
                    website=set(website)
                    print('website is exist  410 ')
                    return website      
        

            # websitefuntext()

            def upcompanyfuntext():
                    #COMPANY NAME

                if companynametext() and mailtext():
                    print(f'companynametext and mailtext is exist 435')
                    listemails=str(mailtext())
                    listemails=listemails.replace("@"," ").replace("."," ").replace('[','').replace(']','')
                    print('427',listemails)

                    # strcompanyname=str(companynametext())

                    companyor='or'.join([f'"{item}"' for item in companynametext()])

                    # print('ckcjnqwduiom qdb',companyor)
                    print('60000',companyor)

                    def find_common(string1,string2):
                        string2_list=string2.split(" ")
                        result=''
                        for item in string2_list:
                            print('607',item)
                            matcher_obj=re.search(item,string1,re.IGNORECASE)# or re.search(string1,item,re.IGNORECASE)
                            print('609',matcher_obj)
                            if matcher_obj is not None:
                                print('611',matcher_obj)
                                result+=string1[matcher_obj.start():matcher_obj.end()]+" "
                        print('613',result)

                        return result
                    # for i in companynametext():
                    var=find_common(companyor,listemails).strip()
                    result =re.sub(r'\b(?:com|in|org|co|net)\b', ' ', var,re.IGNORECASE)   
                    if result:

                        setresult=str(result).split()
                        result=set(setresult)
                        print(f'result is {result}')          
                        return result

                    if not result:               
                        # replacemail=mailtext().replace('@','').replace('.','')
                        getafter_pattern=r'@(\w+)'
                        # result =re.sub(r'\b(?:com|in|org|co|net)\b', ' ', getafter_pattern,re.IGNORECASE)   
                        resultre = re.findall(getafter_pattern, str(mailtext()),re.IGNORECASE)
                        setresult=set(resultre)
                        result=setresult
                        print(' 659 update mail',result)
                        return result
                    
                if not mailtext() and not companynametext() and websitefuntext():
                    print('478 website only',websitefuntext())
                    strwebsite=str(websitefuntext())
                    getafter_pattern=r'www.(\w+)'
                    resultre = re.findall(getafter_pattern, strwebsite,re.IGNORECASE)
                    print('673',resultre)
                    setresult=set(resultre)
                    result=setresult
                    print(' 668 update mail',result)
                    return result

                if not companynametext() and mailtext():
                    print('companynname is still not found')
                    print('673',str(mailtext()))
                    emailsstr=str(mailtext())
                    getafter_pattern=r'@(\w+)'
                    resultre = re.findall(getafter_pattern,emailsstr,re.IGNORECASE)
                    print('675',resultre)
                    setresult=set(resultre)
                    result=setresult
                    print(' 677 update mail',result)
                    return result
                    




            # upcompanyfuntext()

            print('***********************',upcompanyfuntext(),'***********',addresstext(),'*********',contacttext(),'*****************',mailtext(),'*********',websitefuntext(),'******************')


            data = {
            "company_name":str(upcompanyfuntext()).replace('{','').replace('}','').replace('[','').replace(']',''),
            "address":list(addresstext()),#.replace('{','').replace('}','').replace('[','').replace(']',''),
            "contact_number":str(contacttext()).replace('{','').replace('}','').replace('[','').replace(']',''),
            "email": str(mailtext()).replace('{','').replace('}','').replace('[','').replace(']',''),
            "website": str(websitefuntext()).replace('{','').replace('}','').replace('[','').replace(']',''),
            }

            serializer=serializersclass(data=data)
            # print(serializer)
            if serializer.is_valid():
                serializer.save()
                print('saved')
            else:
                print('NOT SAVE')


        return Response(serializer.data)



        
    def get(self,request,*args,**kwargs):
        variable=Company.objects.all()
        serializer=serializersclass(variable,many=True)
        return Response(serializer.data)




