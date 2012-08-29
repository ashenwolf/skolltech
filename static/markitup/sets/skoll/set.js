// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2011 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
// Html tags
// http://en.wikipedia.org/wiki/html
// ----------------------------------------------------------------------------
// Basic set. Feel free to add more tags
// ----------------------------------------------------------------------------
var mySettings = {
	onShiftEnter:  	{keepDefault:false, replaceWith:'<br />\n'},
	onCtrlEnter:  	{keepDefault:false, openWith:'\n<p>', closeWith:'</p>'},
	onTab:    		{keepDefault:false, replaceWith:'    '},
	markupSet:  [ 	
		{name:'Bold', key:'B', openWith:'(!(<strong>|!|<b>)!)', closeWith:'(!(</strong>|!|</b>)!)' },
		{name:'Italic', key:'I', openWith:'(!(<em>|!|<i>)!)', closeWith:'(!(</em>|!|</i>)!)'  },
		{name:'Stroke through', key:'S', openWith:'<del>', closeWith:'</del>' },
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'    <li>', closeWith:'</li>', multiline:true, openBlockWith:'<ul>\n', closeBlockWith:'\n</ul>'},
		{name:'Numeric List', openWith:'    <li>', closeWith:'</li>', multiline:true, openBlockWith:'<ol>\n', closeBlockWith:'\n</ol>'},
		{separator:'---------------' },
//		{name:'Picture', key:'P', replaceWith:'<img src="[![Source:!:http://]!]" alt="[![Alternative text]!]" />' },
		{
			name:'Picture',
			key:'P',
			//beforeInsert: function(markItUp) { InlineUpload.display(markItUp) },
			beforeInsert: function(markItUp) { popupGallery.display(markItUp) },
		},
		{name:'Link', key:'L', openWith:'<a href="[![Link:!:http://]!]"(!( title="[![Title]!]")!)>', closeWith:'</a>', placeHolder:'Your text to link...' },
		{separator:'---------------' },
		{name:'Clean', className:'clean', replaceWith:function(markitup) { return markitup.selection.replace(/<(.*?)>/g, "") } },		
		{name:'Preview', className:'preview',  call:'preview'},
		{separator:'---------------' },
	]
}


var popupGallery = {
	dialog: null,
	block: '',
	offset: {},
	options: {

	},
	display: function(hash) {
		$('#galleryModal').modal();
	},
	cleanUp: function() {

	},
}


var InlineUpload = 
{
	dialog: null,
	block: '',
	offset: {},
	options: {
		container_class: 'markItUpInlineUpload',
		form_id: 'inline_upload_form',
		action: '/posts/upload',
		inputs: {
			classname: { label: 'Class', id: 'inline_upload_class', name: 'inline_upload_class' },
			id: { label: 'ID', id: 'inline_upload_id', name: 'inline_upload_id' },
			alt: { label: 'Alt text', id: 'inline_upload_alt', name: 'inline_upload_alt' },
			file: { label: 'File', id: 'inline_upload_file', name: 'inline_upload_file' }
		},
		submit: { id: 'inline_upload_submit', value: 'upload' },
		close: 'inline_upload_close',
		iframe: 'inline_upload_iframe'
	},
	display: function(hash)
	{		
		var self = this;

		/* Find position of toolbar. The dialog will inserted into the DOM elsewhere
		 * but has position: absolute. This is to avoid nesting the upload form inside
		 * the original. The dialog's offset from the toolbar position is adjusted in
		 * the stylesheet with the margin rule.
		 */
		this.offset = $(hash.textarea).prev('.markItUpHeader').offset();

		/* We want to build this fresh each time to avoid ID conflicts in case of
		 * multiple editors. This also means the form elements don't need to be
		 * cleared out.
		 */
		this.dialog = $([
			'<div class="',
			this.options.container_class,
			'"><div><form id="',
			this.options.form_id,
			'" action="',
			this.options.action,
			'" target="',
			this.options.iframe,
			'" method="post" enctype="multipart/form-data"><label for="',
			this.options.inputs.classname.id,
			'">',
			this.options.inputs.classname.label,
			'</label><input name="',
			this.options.inputs.classname.name,
			'" id="',
			this.options.inputs.classname.id,
			'" type="text" /><label for="',
			this.options.inputs.id.id,
			'">',
			this.options.inputs.id.label,
			'</label><input name="',
			this.options.inputs.id.name,
			'" id="',
			this.options.inputs.id.id,
			'" type="text" /><label for="',
			this.options.inputs.alt.id,
			'">',
			this.options.inputs.alt.label,
			'</label><input name="',
			this.options.inputs.alt.name,
			'" id="',
			this.options.inputs.alt.id,
			'" type="text" /><label for="',
			this.options.inputs.file.id,
			'">',
			this.options.inputs.file.label,
			'</label><input name="',
			this.options.inputs.file.name,
			'" id="',
			this.options.inputs.file.id,
			'" type="file" /><input id="',
			this.options.submit.id,
			'" type="button" value="',
			this.options.submit.value,
			'" /></form><div id="',
			this.options.close,
			'"></div><iframe id="',
			this.options.iframe,
			'" name="',
			this.options.iframe,
			'" src="about:blank"></iframe></div></div>',
		].join(''))
			.appendTo(document.body)
			.hide()
			.css('top', this.offset.top)
			.css('left', this.offset.left);


		/* init submit button
		 */
		$('#'+this.options.submit.id).click(function()
		{
			$('#'+self.options.form_id).submit().fadeTo('fast', 0.2).parent().loading();
		});


		/* init cancel button
		 */
		$('#'+this.options.close).click(this.cleanUp);


		/* form response will be sent to the iframe
		 */
		$('#'+this.options.iframe).bind('load', function()
		{
			var response = $.secureEvalJSON($(this).contents().find('textarea').text());

			if (response.status == 'success')
			{
				this.block = [
					'<img src="',
					response.src,
					'" width="',
					response.width,
					'" height="',
					response.height,
					'" alt="',
					$('#'+self.options.inputs.alt.id).val(),
					'" class="',
					$('#'+self.options.inputs.classname.id).val(),
					'" id="',
					$('#'+self.options.inputs.id.id).val(),
					'" />'
				];

				self.cleanUp();

				/* add the img tag
				 */
				$.markItUp({ replaceWith: this.block.join('') } );
			}
			else
			{
				/* A really basic example. This should do something a bit more sophisticated.
				 */
				alert(response.msg);
				self.cleanUp();
			}
		});

		/* Finally, display the dialog
		 */
		this.dialog.fadeIn('slow');
	},
	cleanUp: function()
	{
		this.dialog.fadeOut().remove();
	}
};