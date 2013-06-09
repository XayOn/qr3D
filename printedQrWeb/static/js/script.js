/* Author:
    David Francos Cuartero
    GPL 2+
*/

function do_qrcode(){
    window.location.href = "/getQr" + "/" + $('#text').val() + "/"+ $('#scale').val();
}


