Title: i'm reading...
Date: %(date)s
Tags: links, %(tags)s
Slug: %(slug)s
Authors: Shaun Martin


{% for a in articles %}
#### [{{ a['title'] }}]({{ a['url'] }})

{% if a['image_url'] %}<div class="left-30">![article image]({{a['image_url']}})</div>{% endif %}
{{a['excerpt']}}

<p class="post-info">
{% for t in a['tags'] %}
  [{{t}}](http://samsite.ca/tag/{{t}}.html)
{% endfor %}
</p>
{% endfor %}
