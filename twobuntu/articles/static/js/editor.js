/**
 * Ace Editor and Toolbar for 2buntu - Copyright 2014 Nathan Osman
 * Released under the Apache License, version 2.1
 */

function Editor(upload_url) {

    // Create the container that will eventually replace the textarea
    var textarea = $('textarea').hide(),
        editor_container = $('<div>', {
            height: textarea.height()
        }).addClass('ace'),
        toolbar = $('<div>').addClass('toolbar'),
        container = $('<div>')
            .addClass('editor')
            .append(toolbar)
            .append(editor_container)
            .insertBefore(textarea);

    // Create the editor (duh!)
    var editor = ace.edit(editor_container[0]);

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

        // Use either an existing selection (if it exists) or supplied text
        text = editor.session.getTextRange(range) || text;

        // Insert the text and then adjust the selection accordingly
        editor.insert(prefix + text + suffix);
        range.setStart(range.start.row, range.start.column + prefix.length);
        range.setEnd(range.start.row, range.start.column + text.length);

        // Set the modified range and focus the editor
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

    // Define the toolbar buttons - note that a separater
    // is defined by an empty element
    var buttons = [
        {
            description: 'Insert bold text',
            icon:        'fa-bold',
            action:      function() { insertText('**', 'text', '**'); },
            key:         { win: 'Ctrl-B', mac: 'Command-B' }
        },
        {
            description: 'Insert italic text',
            icon:        'fa-italic',
            action:      function() { insertText('*', 'text', '*'); },
            key:         { win: 'Ctrl-I', mac: 'Command-I' }
        },
        {},
        {
            description: 'Insert quotation',
            icon:        'fa-quote-left',
            action:      function() { insertText('> ', '"text"', ''); }
        },
        {
            description: 'Insert code',
            icon:        'fa-code',
            action:      function() { insertText('    ', '// printf("Hello, world!");', ''); }
        },
        {},
        {
            description: 'Insert ordered list',
            icon:        'fa-list-ol',
            action:      function() { insertText('1. ', 'Item', '\n    1. Subitem\n    2. Subitem\n2. Item'); }
        },
        {
            description: 'Insert unordered list',
            icon:        'fa-list-ul',
            action:      function() { insertText('* ', 'Item 1', '\n    * Subitem 1\n    * Subitem 2\n* Item 2'); }
        },
        {},
        {
            description: 'Insert link',
            icon:        'fa-link',
            action:      function() { insertText('[', 'link text', '](http://example.org)'); }
        },
        {
            description: 'Insert image',
            icon:        'fa-picture-o',
            action:      function() { insertImage(); }
        },
        {},
        {
            description: 'Insert info',
            icon:        'fa-lightbulb-o',
            action:      function() { insertText('[info]', 'text', '[/info]'); }
        },
        {
            description: 'Insert warning',
            icon:        'fa-exclamation-triangle',
            action:      function() { insertText('[warning]', 'text', '[/warning]'); }
        },
        {
            description: 'Insert danger box',
            icon:        'fa-times-circle',
            action:      function() { insertText('[danger]', 'text', '[/danger]'); }
        }
    ];

    // Append each of the buttons to the toolbar according to
    // the information in the toolbar array
    $.each(buttons, function() {

        if('action' in this) {

            $('<button>')
                .attr('type', 'button')
                .prop('title', this.description)
                .addClass('fa ' + this.icon)
                .click(this.action)
                .appendTo(toolbar);

            // If a keybinding was supplied, then register it
            if('key' in this)
                editor.commands.addCommand({
                    bindKey: this.key,
                    exec: this.action
                });
        } else
            $('<span>')
                .addClass('spacer')
                .appendTo(toolbar);
    });

    // Find the <select> on the page and ensure the editor
    // receives focus when [tab] is pressed
    $('select').keydown(function(event) {

        if(event.which == 9) {
            editor.focus();
            event.preventDefault();
        }
    });
};
