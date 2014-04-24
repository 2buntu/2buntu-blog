/**
 * Markdown Toolbar Buttons & Utils - Copyright 2014 Nathan Osman
 * Released under the Apache License, version 2.0
 */

var Toolbar = {

    'initialize': function() {

        var toolbar = $('<div class="btn-toolbar" role="toolbar"></div>');

        $.each(Toolbar.buttons, function() {

            var group = $('<div class="btn-group btn-group-sm"></div>');

            $.each(this, function() {

                var icon = $('<span class="fa"></span>').addClass(this.icon);
                var btn = $('<button type="button" class="btn btn-default"></button>')
                    .append(icon).attr('title', this.description).click(this.action);

                group.append(btn);
            });

            toolbar.append(group);
        });

        $('#id_body').parents('.row').before(toolbar);

        Toolbar.watchForUnload();
    },

    'watchForUnload': function() {

        var dirty = false;

        $('input[type=text],select,textarea').change(function() { dirty = true; });
        $('button[type=submit]').click(function() { dirty = false; });

        $(window).bind('beforeunload', function() {
            return dirty?true:undefined;
        });
    },

    'insertText': function(pretext, placeholder, posttext) {

        var textarea = $('#id_body')[0];
        var value     = textarea.value,
            sel_start = textarea.selectionStart,
            sel_end   = textarea.selectionEnd;

        textarea.value = value.substring(0, sel_start) +
                         pretext + placeholder + posttext +
                         value.substring(sel_end);

        textarea.selectionStart = sel_start + pretext.length;
        textarea.selectionEnd   = textarea.selectionStart + placeholder.length;
        textarea.focus();
    },

    'insertImage': function() {

        if(arguments.length)
            Toolbar.insertText(arguments[0], '', '');
        else
            window.open(IMAGE_UPLOAD_URL, 'popup', 'width=350,height=330');
    },

    'buttons': [
        [
            {
                'description': 'Insert bold text',
                'icon':        'fa-bold',
                'action':      function() { Toolbar.insertText('**', 'text', '**'); }
            },
            {
                'description': 'Insert italic text',
                'icon':        'fa-italic',
                'action':      function() { Toolbar.insertText('*', 'text', '*'); }
            }
        ],
        [
            {
                'description': 'Insert quotation',
                'icon':        'fa-quote-left',
                'action':      function() { Toolbar.insertText('> ', '"text"', ''); }
            },
            {
                'description': 'Insert code',
                'icon':        'fa-code',
                'action':      function() { Toolbar.insertText('    ', '// printf("Hello, world!");', ''); }
            }
        ],
        [
            {
                'description': 'Insert ordered list',
                'icon':        'fa-list-ol',
                'action':      function() { Toolbar.insertText('1. ', 'Item', '\n    1. Subitem\n    2. Subitem\n2. Item'); }
            },
            {
                'description': 'Insert unordered list',
                'icon':        'fa-list-ul',
                'action':      function() { Toolbar.insertText('* ', 'Item 1', '\n    * Subitem 1\n    * Subitem 2\n* Item 2'); }
            }
        ],
        [
            {
                'description': 'Insert link',
                'icon':        'fa-link',
                'action':      function() { Toolbar.insertText('[', 'link text', '](http://example.org)'); }
            },
            {
                'description': 'Insert image',
                'icon':        'fa-picture-o',
                'action':      function() { Toolbar.insertImage(); }
            }
        ],
        [
            {
                'description': 'Insert info',
                'icon':        'fa-lightbulb-o',
                'action':      function() { Toolbar.insertText('[info]', 'text', '[/info]'); }
            },
            {
                'description': 'Insert warning',
                'icon':        'fa-exclamation-triangle',
                'action':      function() { Toolbar.insertText('[warning]', 'text', '[/warning]'); }
            },
            {
                'description': 'Insert danger box',
                'icon':        'fa-times-circle',
                'action':      function() { Toolbar.insertText('[danger]', 'text', '[/danger]'); }
            }
        ]
    ]
};

$.ready(Toolbar.initialize());
