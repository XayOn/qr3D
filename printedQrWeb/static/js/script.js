window.do_jsqrcode = () ->
    window.location.href = "http://openjscad.org/#" + window.location.href + "getQr" + "/" + $('#text').val() + "/"+ $('#scale').val()
window.do_qrcode = () ->
    window.location.href = window.location.href + "getQrScad" + "/" + $('#text').val() + "/"+ $('#scale').val()

