// Initialisation des variables
var lang1 = '';
var lang2 = '';
var lang_focus = 'lang1';
var url = '';
var pbrunning = false;

function resizewindow () {
    $('#select-tools').children('br').remove();
    if ($(window).width() < 768) {
        console.log('Window resized to mobile');
        $('#select-tools').children().after('<br>');
    }
    else {
        console.log('Window resized to desktop');
    }
}

function setbuttontofilename() { // est appelée apres que l'utilisateur ait choisi un fichier
    filesave();
    var labelSpan = document.getElementById('file-lbl');
    try {
        labelSpan.innerText = files[lang1][0];
    }
    catch (err) {
        return 'No file selected';
    }
    url = ''; // on supprime l'url si l'utilisateur a chargé un fichier
}

function filesave() { // permet de sauvegarder le fichier précédemment chargé par l'utilisateur avant de changer de langage
    // check if a file is loaded
    var file = document.getElementById('file-u').files[0];
    if (!file) {return;} // si aucun fichier n'a été chargé, on ne fait rien
    var filename = file.name;
    files[lang1] = [filename, file];
    console.log("File saved: " + filename + " to " + lang1);
}

function afterlangselection() { // actualise les variables et les extensions en fonction des langages choisis
    lang1 = $('#lang1').text();
    lang2 = $('#lang2').text();

    // si lang1 == HTML ajouter un input permettant d'entrer un url
    if (lang1 == 'HTML') {
        $('#sbar').show(250);
    }
    else {
        $('#sbar').hide(250);
    }
    var exts = extensions[lang1];
    $('#file-u').val('');
    $('#file-u').attr('accept', exts);

    setbuttontofilename();
}

function reverse() { // permet d'inverser les langages
    var lang1 = $('#lang2').text();
    var lang2 = $('#lang1').text();

    $('#lang1').text(lang1);
    $('#lang1').siblings('img').attr('src', icons[lang1]);

    $('#lang2').text(lang2);
    $('#lang2').siblings('img').attr('src', icons[lang2]);

    afterlangselection(); // on actualise les variables et les extensions
}

function displayalert(message, type) { // permet d'afficher une alerte de type 'error' ou 'success'
    messagebox = $('#messagebox');
    progressbar = $('#messagetimer');
    textelt = $('#messagetext');
    caption = $('#captionText');

    if (type == 'error') {
        messagebox.attr('class', 'alert alert-danger mx-auto m-0');
        caption.text('Error: ');
        progressbar.css('background', 'linear-gradient( 135deg, #FEB692 10%, #EA5455 100%)');
    }
    else if (type == 'success') {
        messagebox.attr('class', 'alert alert-success mx-auto m-0');
        caption.text('Success: ');
        progressbar.css('background', 'linear-gradient( 135deg, #ABDCFF 10%, #0396FF 100%)');
    }
    else {
        return;
    }
    textelt.text(message);
    if (!pbrunning) {
        pbrunning = true;
        messagebox.show(250);
        progressbar.animate({width: '100%'}, 2000, 'swing');
        setTimeout(function() {
            messagebox.hide(250);
            progressbar.css('width', '0%');
            pbrunning = false;
        }, 3000);
    }
}

function validateURL() { // est appelée en cas de validation du champ url
    url = document.getElementById('url').value;
    var urlRegex = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    var match = url.match(urlRegex);

    if (!match) {displayalert('Sorry, the entered URL is invalid. Please make sure to enter a valid URL starting with "http://" or "https://".', 'error');}
    else {
      // If 'http' is missing, add 'https://' at the beginning
        url = match[1] ? url : 'https://' + url;
        var hostname = new URL(url).hostname;
        document.getElementById('file-lbl').innerText = hostname;
        displayalert('The URL has been successfully set.', 'success');
    };
}

function send_to_clipboard(divid, type) { // permet de copier le contenu d'un div dans le presse-papier
    // get html of the style with id result-style
    var table_html = '<style>' + $('#result-style').html() + '</style>\n\n';
    
    // in all case, we copy the content of the div with id divid in html we add the style of the table
    if (type == 'html') {
        var content = $('#' + divid).html();
        var content = table_html + content;
    }
    else if (type == 'json') {
        var content = $('#' + divid).text();
    }
    else {
        return;
    }
    try {
        navigator.clipboard.writeText(content);
    }
    catch (err) {
        displayalert('Sorry, we could not copy the content to your clipboard. Please try again.', 'error');
        return;
    }
    displayalert('The content has been copied to your clipboard.', 'success');
}

function startconvert() {
    file = files[lang1][1];

    if (!file && !url) {
        displayalert('Please enter a URL or upload a file.', 'error');
        return;
    }

    if ($('#file-u').val()) {
        var size = file.size;
        if (size > 15000000) {
            displayalert('Sorry, the file is too big. Please make sure to upload a file smaller than 15MB.', 'error');
            return;
        }
    }
    $('#loader').show();

    var data = new FormData();
    data.append('file', file);
    data.append('url', url);
    data.append('from', lang1);
    data.append('to', lang2);

    $.ajax({url: '/', type: 'POST', data: data, contentType: false, processData: false,})

    .done(function(data) {
        // if there is an error in the response, display the error
        if (data['error']) {
            displayalert(data['error'], 'error');
            return;
        }
        // S'il y a un fichier à télécharger, on le télécharge
        else if (data['url']) {
            window.location.href = data['url'];
        }
        else if (data['content']) {
            $('#results').empty();
            if (data['name'] == 'HTML') {
                for (var i = 1; i < data['content'].length; i++) {
                    var div = $('<div class="container position-relative"></div>');
                    var button = $('<button id="copy-btn" class="btn btn-outline-light btn-sm" onclick="send_to_clipboard(\'result' + i + '\', \'html\')">Copy to clipboard</button>');
                    var result = $('<div id="result' + i + '" class="code-block"></div>');
                    content = data['content'][i];

                    result.html(content);
                    div.append(result);
                    div.append(button);
                    $('#results').append(div);
                }
            }
            if (data['name'] == 'JSON') {
                for (var i = 0; i < data['content'].length; i++) {
                    var div = $('<div class="container position-relative"></div>');
                    var button = $('<button id="copy-btn" class="btn btn-outline-light btn-sm" onclick="send_to_clipboard(\'result' + i+1 + '\', \'json\')">Copy to clipboard</button>');
                    var pre = $('<pre class="code-block"></pre>');
                    var code = $('<code id="result' + i+1 + '"></code>');
                    content = data['content'][i];

                    code.text(content);
                    pre.append(code);
                    div.append(pre);
                    div.append(button);
                    $('#results').append(div);

                    hljs.highlightElement(document.getElementById('result' + i+1));
                }
            }
        displayalert(data['success'], 'success')}})
    .fail(function() {displayalert('Internal server error. Please try later.', 'error');})

    .always(function() {$('#loader').hide();});
}

$(document).ready(function() {
    $.ajax({
        url: '/info',
        type: 'POST',
        data: JSON.stringify({}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(data) {
            icons = data['icons'][0];
            formats = data['formats'][0];
            extensions = data['extensions'];
            // files is a dict with key all the formats and value are (name of the file, file)
            files = {};
            for (var i = 0; i < formats.length; i++) {
                files[formats[i]] = ['Import', ''];
            }
        }
    });

    resizewindow(); // A l'initalisation de la page
    $(window).resize(function() {
        resizewindow();
    });

    // On affiche les deux premiers langages
    $('#lang1').text(formats[0]); $('#lang1').siblings('img').attr('src', icons[formats[0]]);
    $('#lang2').text(formats[1]); $('#lang2').siblings('img').attr('src', icons[formats[1]]);
    afterlangselection();

    for (var i = 0; i < formats.length; i++) {
        var lang = formats[i];
        var img = icons[lang];
        var div = $('<div class="btn btn-dark btn-lg mx-auto" id="lang"></div>');
        var img = $('<img src="' + icons[lang] + '">');
        var span = $('<span style="padding-inline: 15px;">' + lang + '</span>');
        div.append(img);
        div.append(span);
        $('.selection').append(div);
    }
    // On click a button with attribute id="select", set the lang_focus to the id of the button
    $(document).on('click', '#select', function() {
        lang_focus = $(this).children('span').attr('id');
        $('.fixed-selection').show();
    });

    $(document).on('click', '#lang', function() { // Permet de savoir si le language de selection est lang1 ou lang2
        // On récupère le langage et l'image du bouton cliqué
        var lang = $(this).children('span').text();
        var img = $(this).children('img').attr('src');

        // Si le langage d'entrée est le même que le langage de sortie, on inverse les langages
        opposite = (lang_focus == 'lang1') ? 'lang2' : 'lang1';
        if (lang == $('#' + opposite).text()) {
            reverse();
            return;
        }

        $('#' + lang_focus).text(lang);
        $('#' + lang_focus).siblings('img').attr('src', img);

        afterlangselection();
    }
    );
});