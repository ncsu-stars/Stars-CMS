function build_tag_cloud(location) {
    $.getJSON(globals.urls.tagCloudUrl, function(data, status, xhr) {
        var container = $('<div id="tagCloud"><ul></ul></div>'),
            tags = { };
        
        tags = data;

        for(var tag in tags) {
            var num = tags[tag],
                tag_html = $('<li class="tag">' + tag + '</li>').css('font-size', function() {
                    if(tags[tag] * 10 < 40) {
                        return tags[tag] * 10 + 'px';
                    } else {
                        return tags[tag] * 5 + 'px';
                    }
                });
            
            container.children('ul').append(tag_html);
        }

        $(location).append(container);
    });
}