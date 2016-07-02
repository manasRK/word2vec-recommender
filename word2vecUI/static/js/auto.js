(function() {
   
    $(document).ready(function() {
        $.ajaxSetup({
            cache: true
        });
        //globals start
        var LEFT_AUTO = -1;
        var FIRST_RESIZE = true;
        var STRLEN = 0;
        var ENABLE_BACKINPUT=true;
        var ORIGINAL_QUERY="";
        var SPACE=false;
        var DEFAULT_LEFT=0;
        
	//globals end

        
        window.searchQuery=function(q) {
            
            window.location = "/search/review/" + encodeURIComponent(q);
        };
        
        //setting up backinput for shadow suggestion
        $(".backinput").remove();
        var BACKINPUT = $("#search").clone();
        BACKINPUT.removeAttr("id");
        BACKINPUT.removeAttr("placeholder");
        BACKINPUT.removeAttr("name");
        BACKINPUT.removeClass("ui-autocomplete-backinput");
       // BACKINPUT.addClass("btn1");
        BACKINPUT.addClass("backinput");
        BACKINPUT.attr("disabled", "");
        
       
            //code for search page
           
            BACKINPUT.attr("id", "input_back");
      
        $("#div_for_back").append(BACKINPUT);
        

        function checkback() {

            //Fixes the issue of backinput on small devices as size is small on typing input scrolls right but backinput remains there only

            if ($(window).width() <= 600) {
                BACKINPUT.val("");
                ENABLE_BACKINPUT = false;
            } else {
                ENABLE_BACKINPUT = true;
            }
            if (($("#search").val().length * 12.5) >= $("#search").width()) {
                BACKINPUT.val("");
                ENABLE_BACKINPUT = false;

            }
        }


        $(window).on("resize", checkback); //check backinput on resize


        checkback(); //init checkback

        $("#search").on("keypress", checkback); //checks backinput when text size exceeds the input


        $("#srmse-logo").on("click", function() {
            window.location = "http://srmsearchengine.in";
        });


        //setting up autocomplete

        //the html autocomplete tweak
        (function($) {
            var proto = $.ui.autocomplete.prototype,
                initSource = proto._initSource;

            function filter(array, term) {
                var matcher = new RegExp($.ui.autocomplete.escapeRegex(term), "i");
                return $.grep(array, function(value) {
                    return matcher.test($("<div>").html(value.label || value.value || value).text());
                });
            }
            $.extend(proto, {
                _initSource: function() {
                    if (this.options.html && $.isArray(this.options.source)) {
                        this.source = function(request, response) {
                            response(filter(this.options.source, request.term));
                        };
                    } else {
                        initSource.call(this);
                    }
                },
                _renderItem: function(ul, item) {
                    return $("<li></li>").data("item.autocomplete", item).append($("<a></a>")[this.options.html ? "html" : "text"](item.label)).appendTo(ul);
                }
            });
        })(jQuery);
function cacheAutocomplete(arr,query){

if(typeof(Storage) !== "undefined") {
   localStorage.setItem("autocomplete#query#"+query,arr);
}

}
        $("#search").autocomplete({
            source:function(request,response){
            function ajaxResponse(){
		    $.ajax({
		  		url: "/autosuggest",
		  		dataType: "text",
                type:"POST",
		  		data: {q:request.term},
		  		success: function(data) {
		      			cacheAutocomplete(data,request.term);
		      			response(JSON.parse(data));
		  		}
	      		});
            }
            	if(typeof(Storage) !== "undefined") {
    			// Code for localStorage/sessionStorage. so first check in cache
    			var item=localStorage.getItem("autocomplete#query#"+request.term);
    			if(item){
    				response(JSON.parse(item));
    			}
    			else{
    				ajaxResponse();
    			}
		}
		else{
			//no localstorage so use ajax
			ajaxResponse();
		}
            
            },
            minLength: 1,
            autoFocus: false,
            appendTo: ".search_div", //setting up the container for the rendered list from autocomplete
            html: true, //tweak done to highlight the searched text
            open: function(event, ui) {
                $('ul.ui-autocomplete').addClass('opened');
                $(".ui-helper-hidden-accessible").remove();
                $(this).autocomplete("widget").css({
                    "width": ($("#search").parent().width() + "px")
                }); //setting up the width of the list to input field useful for responsiveness
                if (LEFT_AUTO !== -1) {
                    $(".ui-autocomplete").css("postion", "relative").css("left", LEFT_AUTO + "px");
                    $(".ui-autocomplete").css("width", "");
              	    $(".ui-autocomplete >li").css("width", "100%");
                    $(".ui-autocomplete >li>a").css("white-space", "nowrap");
                }
                event.preventDefault();
                if($(window).width()<767){
                var big;
                var small;
                	if(LEFT_AUTO!==-1){
                		big=((LAST_WORD_WIDTH)*(0.90)) + "px";
                		small=((LAST_WORD_WIDTH)*(0.10)) + "px";
                	
                	}
                	else{
                		big=($("#search").parent().width()*(0.90)) + "px";
                		small=($("#search").parent().width()*(0.10)) + "px";
                	
                	}
		        $(".ui-menu-item >a").css("width",big).css("float","left");
		        $(".ui-menu-item >a").after("<span class='pen'><span class='glyphicon glyphicon-arrow-up copy_g'></span></span>");
		        $(".pen").css("width",small);
		        $.each($(".pen"),function(index,element){
		        	$(this).css("height",parseInt($(this).parent().find("a").height())+"px");
		        
		        
		        });
                }
                else{
                
                if(LEFT_AUTO!==-1){
				 $(".ui-menu-item >a").css("width",(LAST_WORD_WIDTH) + "px").css("float","left");                	
                	}
                	else{
                	 	$(".ui-menu-item >a").css("width",($("#search").parent().width()) + "px").css("float","left");
                	
                	}
                
                }
            },
            close: function() {
                //clearing up the autocomplete after close 
                $('.ui-menu-item').remove();
                $('ul.ui-autocomplete')
                    .removeClass('opened')
                    .css('display', 'block');
            },
            focus: function(event, ui) {
                if ($("#search").val().trim() !== "") {
                    //checking for resize key in focus 
                    if (ui["item"]["resize"]) {
                        //word suggestion
                        var d = $("#search").val().split(" ");
                        if (ENABLE_BACKINPUT) {
                            BACKINPUT.val((d.slice(0, d.length - 1) + " " + ui["item"]["value"]).replace($("#search").val().toLowerCase(), $("#search").val()));
                        }
                    } else {

                        if (ui["item"]["resize"]) {
                            //sentence suggestion
                            if (ENABLE_BACKINPUT) {
                                BACKINPUT.val(ui["item"]["value"].replace($("#search").val().toLowerCase(), $("#search").val()));
                            }
                        } else {
                            $("#search").val(ui["item"]["value"]);
                            if (ENABLE_BACKINPUT) {
                                BACKINPUT.val(ui["item"]["value"]);
                            }

                        }
                    }
                }


                if (ORIGINAL_QUERY) {
                    if (ORIGINAL_QUERY !== "") {
                        event.preventDefault();
                        var arr = ORIGINAL_QUERY.split(" ");
                        var temp = arr.slice(0, arr.length - 1).join(" ");
                        $("#search").val(temp + " " + ui["item"]["value"]);

                    }
                }




            },
            response: function(event, ui) {

                 var arrr =[];
                if ($("#search").val().trim() !== "") {
                    if (ui.content[0]["resize"] === "true") {
                        //#DEBUGconsole.log("here");
                        arrr = $("#search").val().trim().split(" ");
                        if (ENABLE_BACKINPUT) {
                            BACKINPUT.val(arrr.slice(0, arrr.length - 1).join(" ") + " " + ui.content[0]["value"]);
                        }
                    } else {
                        if (ENABLE_BACKINPUT) {
                            BACKINPUT.val(ui.content[0]["value"].replace($("#search").val().toLowerCase(), $("#search").val()));
                        }
                    }
                }


               // console.log(ui);
                if (ui.content[0]["resize"] === "true") {
                    //#DEBUGconsole.log("here1");
                    ORIGINAL_QUERY = $("#search").val().trim();
                    var pos;
                    if (FIRST_RESIZE) {
                        SPACE = false; //disable multiple space hits to remove of drag effect
                        DEFAULT_LEFT = parseInt($("#search").offset().left);
                        FIRST_RESIZE = false;
                        
                        pos = arrr.slice(0,arrr.length-1).join(" ").length * parseInt($("#search").css("font-size").replace("px", ""));
                        var temp=arrr.pop().length * parseInt($("#search").css("font-size").replace("px", ""));
                        LAST_WORD_WIDTH=temp+100; //adding a 100 px assuming biggest word
                        STRLEN = parseInt(pos) * 0.7;
                        LEFT_AUTO = DEFAULT_LEFT + pos; //setting up new left auto position
                    } else {
                        if (SPACE) {
                            pos = arrr.slice(0,arrr.length-1).join(" ").length * parseInt($("#search").css("font-size").replace("px", ""));
                            var temp=arrr.pop().length * parseInt($("#search").css("font-size").replace("px", ""));
                        LAST_WORD_WIDTH=temp+100;
                            STRLEN = pos * 0.7;
                            LEFT_AUTO =DEFAULT_LEFT + pos;
                            SPACE = false;
                        }
                    }


                } else {
                    ORIGINAL_QUERY = "";
                    LEFT_AUTO = -1;
                }
            },
            select: function(e, ui) {

                e.preventDefault();
               
              

            },
            delay: 300

        });

        function commonTest(event) {
            if ($("#search").val().indexOf(" ") === 0) {
                $("#search").val($("#search").val().replace(/\s+/g, " ").trim()); //blocking multiple spaces in the beginning
            }
            if ($("#search").val().trim() === "") {
                if (ENABLE_BACKINPUT) {
                    BACKINPUT.val("");
                }
            }
            if (event.keyCode !== 39) {
                if (ENABLE_BACKINPUT) {
                    BACKINPUT.val("");
                }
            }
        }

        function submit(event) {
            if ((event.keyCode === 13) && ($("#search").val() !== "")) {
                var query = $("#search").val().trim();
                searchQuery(query);

            }

        }
        $("#search").on("keypress", function(event) {
            commonTest(event);
            submit(event);

        });
        $("#search").on("keyup", function(event) {
            commonTest(event);
            submit(event);
        });
        $("#search").on("keydown", function(event) {
            commonTest(event);
            submit(event);

            if (event.keyCode === 39) {
                if ((document.getElementById('search').selectionStart === $("#search").val().length) && $("#search").val().length < $(".backinput").val().length) {
                    $("#search").val($(".backinput").val());
                }

            } else {
                $(".backinput").val("");
            }

        });

        $("#search_btn").on("click", function() {
            if ($("#search").val().trim() !== "") {
                var query = $("#search").val().trim();
                // var options = document.getElementsByName('options');
                // for(var i = 0; i < options.length; i++){
                //     if(options[i].checked){
                //         opt = options[i].value;
                //         }
                // console.log("opt values " + opt);
                // }
                // var form = document.getElementById("opt");
                // alert(form.elements["opt"].value);
                searchQuery(query);
            }
        });


        $(window).on("resize", function() {

            //hides autocomplete dropdown on screen resize
            $(".ui-autocomplete").hide();
            LEFT_AUTO = -1;
            FIRST_RESIZE = true;
            STRLEN = 0;

        });

        
       
        $("#search").on("keyup", function(event) {
            commonTest(event);
            if (event.keyCode === 32) {
                SPACE = true;
            } else if (event.keyCode === 8) {
                var a = $("#search").val();
                if (a.slice(a.length - 1, a.length) === " ") {
                    if (a.slice(a.length - 2, a.length) === "  ") {
                        SPACE = false;
                    } else {
                        SPACE = true;
                    }

                }
            }
        });
      
    });


})();

(function(){
    $(document).ready(function(){
        $("#search").on("focus",function(){
            $(".search_input_group").attr("style","border : 1px solid #acacac !important");
        });
        $("#search").on("focusout",function(){
            $(".search_input_group").attr("style","");
        });
    });
})();