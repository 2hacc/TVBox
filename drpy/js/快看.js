var rule={
    title:'快看',
    host:'https://www.kuaikanys.net',
    // homeUrl:'/',
    url:'/s/fyclass/page/fypage.html',
    searchUrl:'/vodsearch/-------------.html?wd=**&submit=',
    searchable:2,//是否启用全局搜索,
    quickSearch:1,//是否启用快速搜索,
    filterable:0,//是否启用分类筛选,
    headers:{//网站的请求头,完整支持所有的,常带ua和cookies
        'User-Agent':'MOBILE_UA',
        // "Cookie": "searchneed=ok"
    },
    class_parse:'nav ul li;a&&Text;a&&href;.*/(.*?)\.html',
	cate_exclude:'专题',
    play_parse:true,
    lazy:'',
    limit:6,
    推荐:'.show;ul&&li;*;*;*;*',
    double:true, // 推荐内容是否双层定位
    一级:'.show&&ul&&li;a&&title;img&&src;.score&&Text;a&&href',
    二级:{"title":"h1&&Text;.info&&ul&&p&&Text","img":"img&&src","desc":".info&&ul&&p:eq(-2)&&Text;.info&&ul&&p:eq(-1)&&Text;.info&&ul&&p:eq(0)&&Text;.info&&ul&&p:eq(1)&&Text;.info&&ul&&p:eq(2)&&Text;.info&&ul&&p:eq(3)&&Text","content":".text&&Text","tabs":".play&&span","lists":".playlist&&ul:eq(#id) li"},
    搜索:'*',
    // 搜索:'*;*;*;*;*',
}