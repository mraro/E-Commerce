function previewImagem() {
    var imagem = document.querySelector('#id_cover').files[0];
    var preview = document.querySelector('#preview');

    var reader = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (imagem) {
        reader.readAsDataURL(imagem);
    } else {
        preview.src = "";
    }
}