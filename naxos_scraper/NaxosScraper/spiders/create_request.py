def composer_list_request(letter, page):
    url = "https://www.naxos.com/Composer/AjxGetComposersByLastName"

    headers = {
        "accept": "*/*",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.naxos.com",
        "priority": "u=1, i",
        "referer": f"https://www.naxos.com/Composer/List/?composer_id={letter}&page={page}",
        "sec-ch-ua": ["\"Not/A)Brand\";v=\"8\"", "\"Chromium\";v=\"126\"", "\"Google Chrome\";v=\"126\""],
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    cookies = {
        "ASP.NET_SessionId": "qixpeus3vhfhrazfavtot4t1",
        "__RequestVerificationToken": "6CsmH834-RV0qkNaNKG3sFovb9XMJUy76mr2E43Cx_T-Sre4kjgsmEeyq_eqBClPHqXMOncB2CW_BpaOt2eiX8oi2d41",
        "_tracking_consent": "%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22DEBY%22%2C%22reg%22%3A%22GDPR%22%7D",
        "AWSALB": "5rn4eY117PmyxITuYjDMLNERobovf3Z7sgVmSzwLVsNXVAzoXohiaZM6hF1wTupZxcE2SSGXGpYx0udfutiq22QFKQG6pbWoYpAVqubpyog7O9bHBDEyXQD9zjpT",
        "AWSALBCORS": "5rn4eY117PmyxITuYjDMLNERobovf3Z7sgVmSzwLVsNXVAzoXohiaZM6hF1wTupZxcE2SSGXGpYx0udfutiq22QFKQG6pbWoYpAVqubpyog7O9bHBDEyXQD9zjpT"
    }

    data = {
        "__RequestVerificationToken": "r7yuZxgfudnCbDAuHY3I-IYcYfAq0WNmPqWm2SfQjk3pNuYg--Z6eYLxBPClGqjabJlp3x0jZ308ctYzPeGmCpaHt6U1",
        "letterFilter": letter,
        "page": str(page)
    }

    return url, headers, cookies, data


def album_list_request(name, id, page):
    url = "https://www.naxos.com/Bio/AjxGetBioDiscographyAlbums"

    headers = {
        "accept": "*/*",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.naxos.com",
        "priority": "u=1, i",
        "referer": f"https://www.naxos.com/Bio/Person/{name}/{id}",
        "sec-ch-ua": ["\"Not/A)Brand\";v=\"8\"", "\"Chromium\";v=\"126\"", "\"Google Chrome\";v=\"126\""],
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    cookies = {
        "ASP.NET_SessionId": "qixpeus3vhfhrazfavtot4t1",
        "__RequestVerificationToken": "6CsmH834-RV0qkNaNKG3sFovb9XMJUy76mr2E43Cx_T-Sre4kjgsmEeyq_eqBClPHqXMOncB2CW_BpaOt2eiX8oi2d41",
        "_tracking_consent": "%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22DEBY%22%2C%22reg%22%3A%22GDPR%22%7D",
        "AWSALB": "7uH4yyGqf7iEoZyE8gHYj4bXrLlaL9tOCwn/99EMOLJIn6t9OIPcTFtTl2g6cGybICRsY3w7PUqaT2BpEM4GsJu2ezcx30J7xNo9C8tAeeuad0k9WBVKxUKdVJt1",
        "AWSALBCORS": "7uH4yyGqf7iEoZyE8gHYj4bXrLlaL9tOCwn/99EMOLJIn6t9OIPcTFtTl2g6cGybICRsY3w7PUqaT2BpEM4GsJu2ezcx30J7xNo9C8tAeeuad0k9WBVKxUKdVJt1"
    }

    data = {
        "__RequestVerificationToken": "UjtnQ57Ts9aIWanwE-pmVWlxPIQqs7ji7GU1MR4mzMAtMg7-ahPbB-YD8v52KTn2Au6GcYXm9jw1UegKQKI5WT88_L81",
        "personId": id,
        "personTypeId": "0",
        "page": str(page),
        "sort": "1"
    }

    return url, headers, cookies, data


def album_info_request(catalogue_id):
    url = "https://www.naxos.com/CatalogueDetail/GetContentAlbumInfo"
    
    headers = {
        "accept": "*/*",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.naxos.com",
        "priority": "u=1, i",
        "referer": f"https://www.naxos.com/CatalogueDetail/?id={catalogue_id}",
        "sec-ch-ua": ["\"Not/A)Brand\";v=\"8\"", "\"Chromium\";v=\"126\"", "\"Google Chrome\";v=\"126\""],
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    
    cookies = {
        "ASP.NET_SessionId": "qixpeus3vhfhrazfavtot4t1",
        "__RequestVerificationToken": "6CsmH834-RV0qkNaNKG3sFovb9XMJUy76mr2E43Cx_T-Sre4kjgsmEeyq_eqBClPHqXMOncB2CW_BpaOt2eiX8oi2d41",
        "_tracking_consent": "%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22DEBY%22%2C%22reg%22%3A%22GDPR%22%7D",
        "AWSALB": "uEOi0Pq8hrTJ6qCsDqqW/v++l3NSR1al0bp3/0dU1xssNDrdmpYMUFRvG/EAvEzzwtwjcC98t1YJx0LA83EeiD3GcqGYJjRbumrZq3cPNLIB6zx3XBJd11iZM9vM",
        "AWSALBCORS": "uEOi0Pq8hrTJ6qCsDqqW/v++l3NSR1al0bp3/0dU1xssNDrdmpYMUFRvG/EAvEzzwtwjcC98t1YJx0LA83EeiD3GcqGYJjRbumrZq3cPNLIB6zx3XBJd11iZM9vM"
    }
    
    data = {
        "__RequestVerificationToken": "2sBDVmiSkDfQwIpOXFfoyxuiI-YmumFgO0fvb3qH94qtclP-llVz25LqdXseowQta2w9RrjNt8gZbX2GLEUnsLYRWUE1",
        "catalogueId": catalogue_id
    }
    
    return url, headers, cookies, data