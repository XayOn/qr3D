window.do_jsqrcode = () ->
    window.location.href = "http://openjscad.org/#" + window.location.href + "getQr" + "/" + $('#text').val() + "/"+ $('#scale').val()
