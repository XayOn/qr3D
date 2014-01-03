window.do_qrcode = () ->
    $.ajax "/getQr" + "/" + $('#text').val() + "/"+ $('#scale').val(),
        success: (data, textStatus, jqXHR) ->
            window.location.href = data
            window.thingiview.loadSTL data

($ document) .ready ->
    window.thingiurlbase = "/static/js/"
    window.thingiview = new Thingiview("viewer")
    window.thingiview.setObjectColor('#C0D8F0')
    window.thingiview.initScene();
