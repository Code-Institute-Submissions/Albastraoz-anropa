/* This code is used to insert a piece of text into a textarea at the current position of the cursor */
function inyectarTexto(elemento, valor) {
    var elemento_dom = document.getElementsByName(elemento)[0];
    if (document.selection) {
        elemento_dom.focus();
        sel = document.selection.createRange();
        sel.text = valor;
        return;
    } if (elemento_dom.selectionStart || elemento_dom.selectionStart == "0") {
        var t_start = elemento_dom.selectionStart;
        var t_end = elemento_dom.selectionEnd;
        var val_start = elemento_dom.value.substring(0, t_start);
        var val_end = elemento_dom.value.substring(t_end, elemento_dom.value.length);
        elemento_dom.value = val_start + valor + val_end;
    } else {
        elemento_dom.value += valor;
    }
}

/* This checks if the file that the user is trying to upload is too big */
$('#cv_file').on('change', function () {
    if (this.files[0].size > 1048576) {
        $('#fileToBig').modal('show');
        $(this).val('');
        $(this).next('.custom-file-label').html("Choose file");
    } else {
        var fileName = $(this).val().replace('C:\\fakepath\\', " ");
        $(this).next('.custom-file-label').html(fileName);
    }
})