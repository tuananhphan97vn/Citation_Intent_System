var utag_data={browse_content_type:"",browse_topic:"",content_type:"",course_category_name:"",course_sub_category:"",document_id:"",document_isAbstract:"",document_isDHTML:"",document_isHTML:"",document_pub_id:"",event_name:"",filter_type:"",filter_value:"",link_category:"",link_name:"",publisher:"",search_collection:"",search_keyword:"",search_refinements:"",search_search_within:"",search_results_count:"",search_type:"",sheet_name:"",sheet_type:"",site_section:"",site_section_tab:"",user_id:TEALIUM_userId,user_institution_id:TEALIUM_userInstitutionId,user_product:TEALIUM_products,user_third_party:TEALIUM_user_third_party,user_type:TEALIUM_userType},tealiumConfig={enabled:TEALIUM_CONFIG_TAGGING_ENABLED,tealium_cdn_url:TEALIUM_CONFIG_CDN_URL,account_profile_environment:TEALIUM_CONFIG_ACCOUNT_PROFILE_ENV,suppress_first_view:!0},tealiumAnalytics={config:{defaults:{tagOptions:{allTags:{},pageTagsOnly:{},eventAndLinkTagsOnly:{}}}},data:{data4eventTags:[],data4pageTags:[]},initData:function(t){"use strict";t&&"object"==typeof t&&(this.config=t.config,this.data=t.data),this.config.defaults.tagOptions.pageTagsOnly.func2getTealiumUtagData=this.getTealiumUtagData,this.config.defaults.tagOptions.pageTagsOnly.func2setTealiumUtagData=this.setTealiumUtagData},init:function(){this.initData(tealiumTagsData),this.setTealiumPageTagsValues(jQuery,this.config.defaults.tagOptions.baseAndPageTagsOnly),this.setTealiumEventTagsValues(this.data.data4eventTags,jQuery,this.config.defaults.tagOptions.eventAndLinkTagsOnly)},setTealiumPageTagsValues:function(t,a){var e={useExistingUtagValuesAsBase:!0,dataAttributeName:"tealium_utag_data",actionAttributeName:"tealium_utag_action",setBaseTags:!0,setPageTags:!0,setUserTags:!1,setEventAndLinkTags:!1,jqSelector:".stats-tag-marker-page",func2getTealiumUtagData:tealiumAnalytics.getTealiumUtagData,func2setTealiumUtagData:tealiumAnalytics.setTealiumUtagData};a=t.extend(e,a),tealiumConfig.enabled&&0!==t(a.jqSelector).length&&(this.addSetTealiumUtagData2jQuery(t),t(a.jqSelector).last().setTealiumUtagData(a))},addSetTealiumUtagData2jQuery:function(t){t.fn.setTealiumUtagData=function(a,e){var s={useExistingUtagValuesAsBase:!0,dataAttributeName:"tealium_utag_data",actionAttributeName:"tealium_utag_action",setBaseTags:!0,setPageTags:!0,setUserTags:!0,setEventAndLinkTags:!0,func2getTealiumUtagData:tealiumAnalytics.getTealiumUtagData,func2setTealiumUtagData:tealiumAnalytics.setTealiumUtagData};if((a=t.extend(s,a)).useExistingUtagValuesAsBase&&"boolean"==typeof a.useExistingUtagValuesAsBase){var u=a.func2getTealiumUtagData(t,a);e=t.extend(u,e)}var n=t(this).data(a.dataAttributeName);switch(e=t.extend(e,n),a.func2setTealiumUtagData(e,t,a),t(this).data(a.actionAttributeName)){case"view":utag.view(e);break;case"link":utag.link(e)}}},setTealiumEventTagsValues:function(t,a,e){var s={useExistingUtagValuesAsBase:!0,dataAttributeName:"tealium_utag_data",actionAttributeName:"tealium_utag_action",setBaseTags:!1,setPageTags:!0,setUserTags:!1,setEventAndLinkTags:!1,events:"click",func2getTealiumUtagData:tealiumAnalytics.getTealiumUtagData,func2setTealiumUtagData:tealiumAnalytics.setTealiumUtagData};e=a.extend(s,e),a=a||jQuery,tealiumConfig.enabled&&(t&&0!==t.length?(this.addSetTealiumUtagDataOnEvent2jQuery(a),t.forEach((function(t,s){try{if(0===a(t.jqSelector).length)return;a(t.jqSelector).setTealiumUtagDataOnEvent(t,e)}catch(a){console.error("Will skip an event tag data entry, check its jqSelector value, could not process data4eventTag:",t,". Got error:",a)}}))):console.log("Tealium Event tags from tealiumTagData will not be fired from JSP pages - UnExpected value for data4eventTags:",t))},addSetTealiumUtagDataOnEvent2jQuery:function(t){t.fn.setTealiumUtagDataOnEvent=function(a,e){var s={useExistingUtagValuesAsBase:!0,dataAttributeName:"tealium_utag_data",actionAttributeName:"tealium_utag_action",setBaseTags:!0,setPageTags:!0,setUserTags:!0,setEventAndLinkTags:!0,events:"click",func2getTealiumUtagData:tealiumAnalytics.getTealiumUtagData,func2setTealiumUtagData:tealiumAnalytics.setTealiumUtagData};if(e=t.extend(s,e),a){var u=a.data;if(e.useExistingUtagValuesAsBase&&"boolean"==typeof e.useExistingUtagValuesAsBase){var n=e.func2getTealiumUtagData(t,e);u=t.extend(n,u)}var i=t(this).data(e.dataAttributeName);if(u=t.extend(u,i))return u.link_name||(u.link_name=t(this).text()),a.events||(a.events=e.events),a.func&&"function"==typeof a.func||a.eventFuncMap||(a.func=function(){tealiumAnalytics.link(u)}),this.on(a.events,a.childSelector,u,a.func,a.eventFuncMap);console.warn("Tealium event tagging failure due to unExpected value for data:",u)}}},setTealiumUtagData:function(t,a,e){"use strict";e=(a=a||jQuery).extend({setBaseTags:!0,setPageTags:!0,setUserTags:!0,setEventAndLinkTags:!0},e);var s=!1;return utag_data&&"object"==typeof utag_data&&t&&"object"==typeof t&&(s=!0,e.setBaseTags&&"boolean"==typeof e.setBaseTags&&(utag_data.browse_content_type=t.browse_content_type,utag_data.browse_topic=t.browse_topic,utag_data.content_type=t.content_type,utag_data.course_category_name=t.course_category_name,utag_data.course_sub_category=t.course_sub_category,utag_data.document_id=t.document_id,utag_data.document_isAbstract=t.document_isAbstract,utag_data.document_isDHTML=t.document_isDHTML,utag_data.document_isHTML=t.document_isHTML,utag_data.document_pub_id=t.document_pub_id,utag_data.filter_type=t.filter_type,utag_data.filter_value=t.filter_value,s=!0),e.setEventAndLinkTags&&"boolean"==typeof e.setEventAndLinkTags&&(utag_data.event_name=t.event_name,utag_data.link_category=t.link_category,utag_data.link_name=t.link_name,s=!0),e.setPageTags&&"boolean"==typeof e.setPageTags&&(utag_data.sheet_name=t.sheet_name,utag_data.sheet_type=t.sheet_type,s=!0),e.setBaseTags&&"boolean"==typeof e.setBaseTags&&(utag_data.publisher=t.publisher,utag_data.search_keyword=t.search_keyword,utag_data.search_results_count=t.search_results_count,utag_data.search_type=t.search_type,utag_data.site_section=t.site_section,utag_data.site_section_tab=t.site_section_tab),e.setUserTags&&"boolean"==typeof e.setUserTags&&(utag_data.user_id=t.user_id,utag_data.user_institution_id=t.user_institution_id,utag_data.user_product=t.user_product,utag_data.user_third_party=t.user_third_party,utag_data.user_type=t.user_type,s=!0)),s},getTealiumUtagData:function(t,a){a=(t=t||jQuery).extend({setBaseTags:!0,setPageTags:!0,setUserTags:!0},a);var e=void 0;return utag_data&&"object"==typeof utag_data&&(e={},a.setBaseTags&&"boolean"==typeof a.setBaseTags&&(e.browse_content_type=utag_data.browse_content_type,e.browse_topic=utag_data.browse_topic,e.content_type=utag_data.content_type,e.course_category_name=utag_data.course_category_name,e.course_sub_category=utag_data.course_sub_category,e.document_id=utag_data.document_id,e.document_isAbstract=utag_data.document_isAbstract,e.document_isDHTML=utag_data.document_isDHTML,e.document_isHTML=utag_data.document_isHTML,e.document_pub_id=utag_data.document_pub_id,e.event_name=utag_data.event_name,e.filter_type=utag_data.filter_type,e.filter_value=utag_data.filter_value,e.link_category=utag_data.link_category,e.link_name=utag_data.link_name),a.setPageTags&&"boolean"==typeof a.setPageTags&&(e.sheet_name=utag_data.sheet_name,e.sheet_type=utag_data.sheet_type),a.setBaseTags&&"boolean"==typeof a.setBaseTags&&(e.publisher=utag_data.publisher,e.search_keyword=utag_data.search_keyword,e.search_results_count=utag_data.search_results_count,e.search_type=utag_data.search_type,e.site_section=utag_data.site_section,e.site_section_tab=utag_data.site_section_tab),a.setUserTags&&"boolean"==typeof a.setUserTags&&(e.user_id=utag_data.user_id,e.user_institution_id=utag_data.user_institution_id,e.user_product=utag_data.user_product,e.user_third_party=utag_data.user_third_party,e.user_type=utag_data.user_type)),e},view:function(t){utag.view(t)},link:function(t){return utag.link(t),!0}};jQuery((function(){tealiumAnalytics.init()}));