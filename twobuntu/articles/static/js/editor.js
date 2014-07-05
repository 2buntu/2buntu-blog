/**
 * Ace Editor and Toolbar for 2buntu - Copyright 2014 Nathan Osman
 * Released under the Apache License, version 2.1
 */

function Editor(upload_url) {

    // Create the container that will eventually replace the textarea
    var width = $('textarea').outerWidth(),
        textarea = $('textarea').hide(),
        container = $('<div>', {
            width: width,
            height: textarea.outerHeight()
        }).css({
            border: '1px solid #ccc'
        }).insertBefore(textarea);

    // Create the editor (duh!)
    var editor = ace.edit(container[0]);

    // Load the value of the textarea
    editor.session.setValue(textarea.val());
    // Enable word-wrap
    editor.session.setUseWrapMode(true);
    // Load the Markdown syntax highlighter
    editor.getSession().setMode('ace/mode/markdown');
    // Hide the gutter (line numbers, etc.)
    editor.renderer.setShowGutter(false);
    // ...and make the font a reasonable size
    editor.setFontSize('12pt');

    // Ensure that the user is warned when they try to
    // close the editor with unsaved changes
    var dirty = false;
    editor.on('change', function() { dirty = true; })
    $(window).bind('beforeunload', function() {
        return dirty ? true : undefined;
    });

    // Also ensure that the editor's contents are dumped
    // into the textarea when the form is submitted
    textarea.closest('form').submit(function() {

        textarea.val(editor.session.getValue());

        // This prevents the unsaved popup
        dirty = false;
    });

    // Inserts the specified text into the editor, setting
    // the current selection to the second parameter
    function insertText(prefix, text, suffix) {

        var selection = editor.getSelection(),
            range = selection.getRange();
        editor.insert(prefix + text + suffix);
        range.setStart(range.start.row, range.start.column + prefix.length);
        range.setEnd(range.start.row, range.start.column + text.length);
        selection.setSelectionRange(range);
        editor.focus();
    }

    // Dual-purpose function: when called with no arguments,
    // it opens a popup for uploading an image; when called
    // with one argument, it is assumed to be an image to
    // insert into the editor
    var insertImage = this.insertImage = function(image) {

        if(image === undefined)
            window.open(upload_url, 'popup', 'width=350,height=330');
        else {
            editor.insert(image);
            editor.focus();
        }
    }

    // Define the toolbar buttons
    var buttons = [
        {
            'description': 'Insert bold text',
            'icon':        'fa-bold',
            'action':      function() { insertText('**', 'text', '**'); }
        },
        {
            'description': 'Insert italic text',
            'icon':        'fa-italic',
            'action':      function() { insertText('*', 'text', '*'); }
        },
        {
            'description': 'Insert quotation',
            'icon':        'fa-quote-left',
            'action':      function() { insertText('> ', '"text"', ''); }
        },
        {
            'description': 'Insert code',
            'icon':        'fa-code',
            'action':      function() { insertText('    ', '// printf("Hello, world!");', ''); }
        },
        {
            'description': 'Insert ordered list',
            'icon':        'fa-list-ol',
            'action':      function() { insertText('1. ', 'Item', '\n    1. Subitem\n    2. Subitem\n2. Item'); }
        },
        {
            'description': 'Insert unordered list',
            'icon':        'fa-list-ul',
            'action':      function() { insertText('* ', 'Item 1', '\n    * Subitem 1\n    * Subitem 2\n* Item 2'); }
        },
        {
            'description': 'Insert link',
            'icon':        'fa-link',
            'action':      function() { insertText('[', 'link text', '](http://example.org)'); }
        },
        {
            'description': 'Insert image',
            'icon':        'fa-picture-o',
            'action':      function() { insertImage(); }
        },
        {
            'description': 'Insert info',
            'icon':        'fa-lightbulb-o',
            'action':      function() { insertText('[info]', 'text', '[/info]'); }
        },
        {
            'description': 'Insert warning',
            'icon':        'fa-exclamation-triangle',
            'action':      function() { insertText('[warning]', 'text', '[/warning]'); }
        },
        {
            'description': 'Insert danger box',
            'icon':        'fa-times-circle',
            'action':      function() { insertText('[danger]', 'text', '[/danger]'); }
        }
    ];

    // Now create the toolbar and insert it directly before the editor
    var toolbar = $('<div>').css({
            backgroundColor: '#ccc'
        }).insertBefore(container);

    // Create the buttons for the toolbar
    $.each(buttons, function() {

        $('<button>', {
            title: this.title,
            type: 'button'
        }).css({
            width: '32px',
            height: '32px'
        }).addClass('fa ' + this.icon).click(this.action).appendTo(toolbar);
    });
};

