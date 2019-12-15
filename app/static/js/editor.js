var toolbarOptions = [
        ['bold', 'italic', 'underline'],        // toggled buttons
        ['blockquote', 'code-block'],

        [{ 'color': [] }],          // dropdown with defaults from theme

        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'align': [] }],

        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

        [{ 'font': [] }],
        [ 'image'],
        ['clean']                                         // remove formatting button
        ];

        var quill = new Quill('#editor', {
        modules: {
                toolbar: toolbarOptions
            },
            theme: 'snow'
        });

        $("#create").click(function(){

                $.ajax({
                url: '/compose/new',
                type: 'POST',
                data: {
                    text: quill.container.firstChild.innerHTML,
                    title: $("#title").val(),
                    tags: $("#tags").val(),
                },
                success: function(result) {
                    window.location.href = '/book/'+result.book_title+'/parts/'+ result.book_id;
                },
                });
            });


              $("#next").click(function(){

                $.ajax({
                url: '/page/save/'+pageId,
                type: 'POST',
                data: {
                    content: quill.container.firstChild.innerHTML, title: $("#title").val(),
                    path_id: pathId,
                    page_id: pageId
                },
                success: function(result) {
                    console.log(result);
                    pageId = 'new';
                    if(pageId == 'new'){
                        history.pushState({}, null, "../../page/new/"+pathId);
                    }
                    quill.setContents([{ insert: '\n' }]);
                },
                });
            });

            $("#save").click(function(){

                $.ajax({
                url: '/page/save/'+pageId,
                type: 'POST',
                data: {
                    content: quill.container.firstChild.innerHTML, title: $("#title").val(),
                    path_id: pathId,
                    page_id: pageId
                },
                success: function(result) {
                    pageId = result.page_id
                    if(pageId == 'new'){
                        history.pushState({}, null, "../../page/"+result.page_id);
                    }

                },
                });
            });

            $("#pages").click(function(){
                window.location.href = '/book/Macera-Tuneli/pages/'+ pathId;
            });

            $(document).keydown(function(e) {
                // {# For ctrl+S #}
                var key = undefined;
                var possible = [ e.key, e.keyIdentifier, e.keyCode, e.which ];

                while (key === undefined && possible.length > 0) {
                    key = possible.pop();
                }

                if (key && (key == '115' || key == '83' ) && (e.ctrlKey || e.metaKey) && !(e.altKey)) {
                    e.preventDefault();
                    $.ajax({
                        url: '/page/save/'+pageId,
                        type: 'POST',
                        data: {
                            content: quill.container.firstChild.innerHTML, title: $("#title").val(),
                            path_id: pathId,
                            page_id: pageId
                        },
                        success: function(result) {
                            alert("Saved");
                        },
                    });
                    return false;
                }
                return true;
            });