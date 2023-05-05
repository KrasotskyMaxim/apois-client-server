<style>
    .button_create {
      display: inline-block;
      padding: 10px 20px;
      background-color: green;
      color: white;
      text-align: center;
      text-decoration: none;
      font-size: 16px;
      border-radius: 5px;
    }
    .button_edit {
        display: inline-block;
        padding: 10px 20px;
        background-color: blue;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        border-radius: 5px;
      }
    .button_delete {
        display: inline-block;
        padding: 10px 20px;
        background-color: red;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        border-radius: 5px;
      }
</style>

<h2>List of {{model}}</h2>

<ul>
% for data in data_list:
    <li>
    % for x in data:
        % if x != data["id"]:
            <i>{{x}}</i>
        % end 
    % end
    </li>    
% end
</ul>

<a href="/{{model}}/create/" class="button_create">Create</a>
<a href="/{{model}}/edit/" class="button_edit">Edit</a>
<a href="/{{model}}/delete/" class="button_delete">Delete</a>
<br>
<br>
<a href="/">home</a>