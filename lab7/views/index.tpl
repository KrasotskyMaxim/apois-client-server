<h2>Home</h2>
<ul>
% for model in models.values():
    <li><a href="/{{model}}/get/">{{model}}</a></li>
% end
</ul>