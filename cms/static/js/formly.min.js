(function($)
{$.fn.formly=function(options,callback)
{var settings={'theme':'Base','onBlur':true};if(options)
{$.extend(settings,options);}
var formName=this.attr('id');if(!formName)
{formName=Math.ceil(Math.random()*5000);this.attr('id',formName);}
this.append('<div style="clear:both;"></div><div class="formlyAlerts"></div>');this.addClass('formlyWrapper-'+settings['theme']);if(this.attr('width'))
{this.css('width',this.attr('width'));}
if(this.attr('subtitle')||this.attr('title'))
{this.prepend('<hr/>');}
if(this.attr('subtitle'))
{this.prepend('<h2>'+this.attr('subtitle')+'</h2>');}
if(this.attr('title'))
{this.prepend('<h1>'+this.attr('title')+'</h1>');}
this.children().each(function(index,item)
{if($(item).attr('place'))
{if($(item).attr('type')=='password')
{var hID='pwPlace-'+$(item).attr('name');$(item).after('<input type="text" id="'+hID+'" value="'+$(item).attr('place')+'" class="formlyPWPlaces" />');$('#'+hID).css('color','#bbb');$(item).hide();$('#'+hID).show();$('#'+hID).focus(function()
{$('#'+hID).hide();$(item).show();$(item).focus();});$(item).blur(function()
{if(!$(item).val())
{$('#'+hID).show();$(item).hide();}});}
else
{$(item).val($(item).attr('place'));$(item).css('color','#bbb');}}
$(item).blur(function()
{if(!$(item).val()||$(item).val()==$(item).attr('pre-fix'))
{if($(item).attr('type')!='password')
{$(item).val($(item).attr('place'));$(item).css('color','#bbb');}}
if($(item).attr('pre-fix'))
{var originalVal=$(item).val();var thePrefix=$(item).attr('pre-fix');if(thePrefix.length==1)
{if(originalVal.charAt(0)!=thePrefix&&$(item).val()!=$(item).attr('place'))
{$(item).val(thePrefix+originalVal);}}
else
{if(originalVal.indexOf(thePrefix)==-1&&$(item).val()!=$(item).attr('place'))
{$(item).val(thePrefix+originalVal);}}}
if(settings['onBlur'])
{if($(item).attr('validate'))
{functions.validate(item);}
if($(item).attr('require'))
{functions.require(item);}
if($(item).attr('match'))
{functions.match(item);}}});$(item).focus(function()
{if($(item).attr('place'))
{if($(item).val()==$(item).attr('place'))
{$(item).val('');$(item).css('color','');}}
if($(item).attr('pre-fix')&&!$(item).val())
{$(item).val('');$(item).val($(item).attr('pre-fix'));}});$('#'+formName).find('input:reset').click(function(item)
{item.preventDefault();$('#'+formName).find('input:text, input:password, input:checkbox, input:radio').each(function()
{$(this).css('border-color','');if($(this).is(':checked'))
{$(this).attr('checked',false);}
if($(this).attr('place'))
{if($(this).attr('type')!='password')
{$(this).val($(this).attr('place'));$(this).css('color','#bbb');}
else
{if($(this).hasClass('formlyPWPlaces'))
{$(this).show();$(this).prev('input').hide();}
else
{$(this).val('');}}}
else
{if($(this).hasClass('formlyPWPlaces'))
{$(this).show();$(this).prev('input').hide();}
else
{$(this).val('');}}});$('#'+formName).find('.formlyAlert').each(function()
{$(this).fadeOut(function()
{$(this).remove()});});});});this.submit(function(item)
{var canSubmit=true;$(this).find('input').each(function()
{if($(this).attr('require'))
{if(!functions.require(this))
{canSubmit=false;}}
if($(this).attr('validate'))
{if(!functions.validate(this))
{canSubmit=false;}}
if($(this).attr('match'))
{if(!functions.match(this))
{canSubmit=false;}}});if(!canSubmit)
{item.preventDefault();}
else
{if(callback)
{item.preventDefault();callback($(this).serialize());}}});var functions={validateString:function(type,string)
{if(type=='email')
{var filter=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i
if(filter.test(string))
{return true;}
else
{return false;}}
else if(type=='http')
{var filter=/http:\/\/[A-Za-z0-9\.-]{3,}\.[A-Za-z]{2,3}/i
if(filter.test(string))
{return true;}
else
{return false;}}},validate:function(item)
{var alertName=formName+$(item).attr('name');if($(item).attr('validate')=='email')
{var valid=functions.validateString('email',$(item).val());var validType='email address';}
else if($(item).attr('validate')=='http')
{var valid=functions.validateString('http',$(item).val());var validType='web address';}
if(!valid)
{if(!$('#'+alertName).is(':visible'))
{$('#'+formName).find('.formlyAlerts').append('<div class="formlyInvalid formlyAlert" id="'+alertName+'">Invalid '+validType+'</div>')
$('#'+alertName).fadeIn();}
var borderColor=$('#'+alertName).css('background-color');$(item).css('border-color',borderColor);if($(item).attr('type')=='password')
{$(item).next('.formlyPWPlaces').css('border-color',borderColor);}
return false;}
else
{$('#'+alertName).fadeOut(function()
{$(this).remove()});$(item).css('border-color','');$('.formlyPWPlaces').css('border-color','');return true;}},require:function(item)
{var alertName=formName+$(item).attr('name');var label=$(item).attr('label')+' ';if(label=='undefined '){label='';}
if(!$(item).val()||$(item).val()==$(item).attr('place'))
{if(!$('#'+alertName).is(':visible'))
{$('#'+formName).find('.formlyAlerts').append('<div class="formlyRequired formlyAlert" id="'+alertName+'">'+label+'Required</div>')
$('#'+alertName).fadeIn();}
var borderColor=$('#'+alertName).css('background-color');$(item).css('border-color',borderColor);if($(item).attr('type')=='password')
{$(item).next('.formlyPWPlaces').css('border-color',borderColor);}
return false;}
else if($(item).attr('type')=='checkbox'&&!$(item).is(':checked'))
{if(!$('#'+alertName).is(':visible'))
{$('#'+formName).find('.formlyAlerts').append('<div class="formlyRequired formlyAlert" id="'+alertName+'">'+label+'Required</div>')
$('#'+alertName).fadeIn();$(item).focus();}
var borderColor=$('#'+alertName).css('background-color');$(item).css('border-color',borderColor);return false;}
else
{$('#'+alertName).fadeOut(function()
{$(this).remove()});$(item).css('border-color','');$('.formlyPWPlaces').css('border-color','');return true;}},match:function(item)
{var alertName=formName+$(item).attr('name');var label=$(item).attr('label')+' ';if(label=='undefined '){label='';}
var toMatch=$(item).attr('match');if($(item).val()!=$('#'+formName).find('input[name='+toMatch+']').val()||!$(item).val())
{if(!$('#'+alertName).is(':visible'))
{$('#'+formName).find('.formlyAlerts').append('<div class="formlyInvalid formlyAlert" id="'+alertName+'">'+label+'Does not match</div>')
$('#'+alertName).fadeIn();}
var borderColor=$('#'+alertName).css('background-color');$(item).css('border-color',borderColor);if($(item).attr('type')=='password')
{$(item).next('.formlyPWPlaces').css('border-color',borderColor);}
return false;}
else
{$('#'+alertName).fadeOut(function()
{$(this).remove()});$(item).css('border-color','');$('.formlyPWPlaces').css('border-color','');return true;}}};};})(jQuery);