/**!
 * @license Markdown-Tag - Add Markdown to any HTML using a <md> tag
 * LICENSED UNDER GPL-3.0 LICENSE
 * MARKDOWN FLAVOUR: GITHUB FLAVORED MARKDOWN. 
 * MORE INFO / FLAVOR OPTIONS CAN BE FOUND AT https://github.com/MarketingPipeline/Markdown-Tag/
*/


/* Const Variables */
// addSyntaxHighlightCss()
var src_syntax_highlight_css = "https://cdn.jsdelivr.net/gh/PrismJS/prism-themes@1.9.0/themes/prism-one-dark.css";
// script / addSyntaxHighlighter()
var src_syntax_highlight = "https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.js";
// addCss()
var src_css = "https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Tag/stylesheets/github_md.min.css";
// loadMarkdownParser()
var src_showdown = "https://cdn.jsdelivr.net/gh/MarketingPipeline/Markdown-Elements/parsers/showdown.min.js";


/* Convert Markdown Tags */ 
function renderMarkdown() {
    /* Add Github CSS + Syntax Highlight CSS  */  
    function addCss() {
        var head = document.head;
        var link = document.createElement("link");

        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = src_css;

        head.appendChild(link);
    }


    function addSyntaxHighlightCss() {
        var head = document.head;
        var link = document.createElement("link");

        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = src_syntax_highlight_css;

        head.appendChild(link);
    }
    

    if (document.getElementsByTagName("md").length > 0) {
        addSyntaxHighlighter();
  
        var converter = new showdown.Converter()   

        converter.setOption('tables', 'on')			
        converter.setOption('emoji', 'on')
        converter.setOption('strikethrough', 'on');
        converter.setOption('tasklists', 'true');
        converter.setOption('ghMentions', 'true');
        converter.setOption('simplifiedAutoLink', 'true');
    
        var converter = new showdown.Converter();
        MD_TAG = document.getElementsByTagName("md");
        
        for(var i=0; i<MD_TAG.length; i++)
            MD_TAG[i].innerHTML = converter.makeHtml(MD_TAG[i].innerHTML)
    }

    
    if (document.getElementsByTagName("github-md").length > 0) {
        addCss();  
        addSyntaxHighlightCss();
  
        addSyntaxHighlighter();

        var converter = new showdown.Converter()

        converter.setOption('tables', 'on')	
        converter.setOption('emoji', 'on')
        converter.setOption('strikethrough', 'on');
        converter.setOption('tasklists', 'true');
        converter.setOption('ghMentions', 'true');
        converter.setOption('simplifiedAutoLink', 'true');
  
        GitHub_MD_TAG = document.getElementsByTagName("github-md");
        
        /* Replace is for temp fix for Gitub Block Quotes */
        for(var i=0; i<GitHub_MD_TAG.length; i++)
            GitHub_MD_TAG[i].innerHTML = converter.makeHtml(GitHub_MD_TAG[i].innerHTML.replace(/&gt;/g, '>'));
    }
}


function addSyntaxHighlighter() {
    // Add Prism.JS to document
    var script = document.createElement('script');
    script.src = src_syntax_highlight;

    document.head.appendChild(script); 
  
    // On Error Loading Markdown Parser
    script.onerror = function () {
        console.error("Markdown Tag: Error while performing function addSyntaxHighlighter - There was an error loading the Syntax Highlighter");
    }
}


function loadMarkdownParser(){
    // Add Markdown Parser To Document
    var script = document.createElement('script');
    script.src = src_showdown;

    //or something of the likes  
    document.head.appendChild(script);
  
    // On Error Loading Markdown Parser
    script.onerror = function () {
        console.error("Markdown Tag: Error while performing function LoadMarkdownParser - There was an error loading the Markdown Parser");
    }

    // Markdown Parser Load Successful 
    script.onload = function () {
        // Let the Magic Begin 
        renderMarkdown()
    };
}


loadMarkdownParser();
