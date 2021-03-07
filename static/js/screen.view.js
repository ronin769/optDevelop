! function (n) {
    var r = {};

    function i(e) {
        if (r[e])
            return r[e].exports;
        var t = r[e] = {
            i: e,
            l: !1,
            exports: {}
        };
        return n[e].call(t.exports, t, t.exports, i),
            t.l = !0,
            t.exports
    }
    i.m = n,
        i.c = r,
        i.d = function (e, t, n) {
            i.o(e, t) || Object.defineProperty(e, t, {
                enumerable: !0,
                get: n
            })
        },
        i.r = function (e) {
            "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
                    value: "Module"
                }),
                Object.defineProperty(e, "__esModule", {
                    value: !0
                })
        },
        i.t = function (t, e) {
            if (1 & e && (t = i(t)),
                8 & e)
                return t;
            if (4 & e && "object" == typeof t && t && t.__esModule)
                return t;
            var n = Object.create(null);
            if (i.r(n),
                Object.defineProperty(n, "default", {
                    enumerable: !0,
                    value: t
                }),
                2 & e && "string" != typeof t)
                for (var r in t)
                    i.d(n, r, function (e) {
                            return t[e]
                        }
                        .bind(null, r));
            return n
        },
        i.n = function (e) {
            var t = e && e.__esModule ? function () {
                    return e.default
                } :
                function () {
                    return e
                };
            return i.d(t, "a", t),
                t
        },
        i.o = function (e, t) {
            return Object.prototype.hasOwnProperty.call(e, t)
        },
        i.p = "",
        i(i.s = 134)
}({
    134: function (e, t, n) {
        "use strict";
        n.r(t);
        var r = n(5),
            i = n.n(r),
            o = n(9),
            s = n(135),
            a = $('<div id="loading" style="display:none;z-index:2000;position:fixed;left:0;right:0;top:0;bottom:0;background:rgba(255,255,255,.3) url(https://activityres.jhm2012.com/gallery119/201812/2054159359.gif) no-repeat center;"></div>').appendTo("body");
        s.init("validate"),
            n(27),
            n(136);
        var u = $(".form");

        //表单提交
        $(".sub_y").on("click", function () {
            if ("true" != $(this).attr("isclick"))
                return !1;
            $("[necessary]", u).validate() ? ($(this).attr("isclick", "false"),
                a.show(),
                $.ajax({
                    url: pageConf.subData.url,
                    type: pageConf.subData.type,
                    data: {
                        user_name: $(".form .item .name").val(),
                        mobile: $(".tel").val(),
                        code: $(".telCode").val()
                    },
                    dataType: "json",
                    success: function (e) {
                        console.log('成功')
                        if(e.result == 'succ'){
                            /*var prize_str = "";
                            $.each(e.info.data,function(index,element){
                                console.log(element);
                                prize_str+="<li><image src='"+element.pic_url+"'/><p>"+element.prize_name+"</p></li>";
                            });
                            $('#prize_data').prepend(prize_str);*/
                            a.hide();
                            $("#success").removeClass("none");
                        }else{
                            a.hide();
                            o(e.reason);
                        }
                    },
                    error: function () {
                        a.hide(),
                            o("网络错误！"),
                            $(this).attr("isclick", "true")
                    }
                })) : $(this).attr("isclick", "true")
            });
            $('#newBtnShare').on("click",function(){
                var shareModal = $("#shareModal");
                if(is_draw_show == 1){
                    $.ajax({
                        url: pageConf.drawData.url,
                        type: pageConf.drawData.type,
                        data: {},
                        dataType: "json",
                        success: function (e) {
                            console.log('成功')
                            if(e.result == 'succ'){
                                is_draw_show = 0;
                                $('#newBtnShare').html('立即分享');
                                a.hide();
                                o(e.info.msg);
                            }else{
                                a.hide();
                                o(e.reason);
                            }
                        },
                        error: function () {
                            a.hide(),
                                o("网络错误！"),
                                $(this).attr("isclick", "true")
                        }
                    });
                }else{
                    shareModal.show();
                }
            });
    },
    135: function (e, t, n) {
        var u = window.jQuery || window.Zepto,
            i = n(9),
            o = void 0;

        function a(e, t, n) {
            var r;
            e || ((t = t || u(this).attr("errormsg")) && i && (r = i.call(this, t, n)),
                !1 !== r && u(this).focus());
            return o && o.call(this, e, t, n),
                e
        }

        function r(n) {
            return function () {
                var e = u(this).val(),
                    t = !e || n.test(e);
                return a.call(this, t, "", {
                    type: "regExp",
                    exp: n
                })
            }
        }
        var c = {
            attrs: {
                necessary: "required",
                required: "required",
                regexp: "regexp"
            },
            vtypes: {
                mobile: "mobile",
                phone: "mobile",
                zipcode: "zipcode",
                identityid: "identityid",
                idcard: "identityid",
                integer: "integer",
                number: "integer",
                email: "email",
                len: "len",
                size: "size"
            }
        };
        c.rules = {
                mobile: /^1[3-9][0-9]\d{8}$/,
                zipcode: /^\d{6}$/,
                identityid: /(^\d{18}$)|(^\d{17}(\d|X|x)$)/,
                email: /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/,
                required: function () {
                    var e = u(this).attr("emptymsg");
                    if ("checkbox" == u(this).attr("type")) {
                        var t = u(this).prop("checked");
                        return a.call(this, t, e, {
                            type: "required"
                        })
                    }
                    if ("radio" == u(this).attr("type")) {
                        t = !1;
                        return u('input[name="' + u(this).attr("name") + '"]').each(function () {
                                if (u(this).prop("checked"))
                                    return a.call(this, t = !0, e, {
                                        type: "required"
                                    })
                            }),
                            a.call(this, t, e, {
                                type: "required"
                            })
                    }
                    t = 0 < (u(this).val() || "").trim().length;
                    return a.call(this, t, e, {
                        type: "required"
                    })
                },
                regexp: function (e) {
                    return r(new RegExp(e)).call(this)
                },
                integer: function (e, t) {
                    void 0 === e && (e = -1 / 0),
                        void 0 === t && (t = 1 / 0);
                    var n = u(this).val().trim(),
                        r = parseInt(n);
                    return a.call(this, n == r && e <= r && r <= t, "", {
                        type: "integer",
                        min: e,
                        max: t
                    })
                },
                len: function (e, t) {
                    void 0 === e && (e = -1 / 0),
                        void 0 === t && (t = 1 / 0);
                    var n = u(this).val().length;
                    return a.call(this, e <= n && n <= t, "", {
                        type: "len",
                        min: e,
                        max: t,
                        len: n
                    })
                },
                size: function (e, t, n) {
                    void 0 === e && (e = 0),
                        void 0 === t && (t = 1 / 0),
                        void 0 === n && (n = 1);
                    var r = u(this).val(),
                        i = r.match(/[\x00-\xff]/g),
                        o = 0;
                    i && (o = i.length);
                    var s = (2 * r.length - o) * n;
                    return a.call(this, e <= s && s <= t, "", {
                        type: "size",
                        min: e,
                        max: t,
                        scale: n,
                        len: s
                    })
                }
            },
            c.prefix = "sv_",
            c.init = function (e) {
                for (var t in c.prefix = e + "_",
                        c.rules) {
                    var n = c.rules[t];
                    u.fn[c.prefix + t] = "function" == typeof n ? n : r(n)
                }
                u.fn[e] = function () {
                    var a = 0;
                    return u(this).each(function () {
                            if (!u(this).attr("vignore")) {
                                for (var e in c.attrs) {
                                    var t = c.prefix + c.attrs[e],
                                        n = u(this).attr(e);
                                    if ("string" == typeof n && !u(this)[t](n))
                                        return !1
                                }
                                var r = u(this).attr("vtype");
                                if (r) {
                                    var i = r.split("|"),
                                        o = c.vtypes[i[0]],
                                        s = i.slice(1);
                                    if (o && (o = c.prefix + o),
                                        o && !u(this)[o].apply(this, s))
                                        return !1
                                }
                            }
                            a++
                        }),
                        a >= u(this).length
                }
            },
            e.exports = {
                instance: c,
                init: function (e) {
                    return e = e || "sv",
                        c.init(e),
                        this
                },
                fnTips: function (e) {
                    return i = e,
                        this
                },
                fnComplete: function (e) {
                    return o = e,
                        this
                }
            }
    },
    136: function (e, t) {
        function u(e) {
            return (u = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
                    return typeof e
                } :
                function (e) {
                    return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
                }
            )(e)
        }! function (c, e) {
            if (e in c)
                throw new Error(["already '", e, "' in 'window'"].join(""));

            function l(e) {
                switch (u(e)) {
                    case "undefined":
                        return "";
                    case "boolean":
                        return e ? "true" : "";
                    case "string":
                        return e.replace(/^\s+|\s+$/g, "");
                    case "number":
                        return e.toString();
                    case "object":
                        return l(e || "");
                    case "function":
                        return l(e())
                }
            }

            function f(e, t) {
                for (var n = e.length, r = 0; r < t.length; r++) {
                    var i = e.indexOf(t[r]);
                    0 <= i && i < n && (n = i)
                }
                return n
            }

            function h(e) {
                for (; e !== (e = e.replace(/((\/|^)[^\/]+\/\.\.)|^\/\.\.|^\.\./g, ""));)
                ;
                return e
            }

            function p(e) {
                if (/^[^#][^?#]*[?#]/.test(e))
                    throw new Error('Argument format is invalid. from string : "' + e + '"');
                "?" === (e = l(e)).charAt(0) && (e = e.substr(1));
                var t = {};
                if ("&" === e.charAt(0) && (t[""] = "",
                        e = e.substr(1)),
                    "" === e)
                    return t;
                var n = e.match(/[?]?[^=&]+=[^=&]+/g);
                if (null == n)
                    return t;
                for (var r = 0; r < n.length; r++)
                    try {
                        var i = n[r].split("=");
                        o(t, decodeURIComponent(i[0]), decodeURIComponent(i[1]))
                    } catch (e) {}
                return t;

                function o(t, e, n) {
                    for (var r = /\[([0-9]*)\]|\[([^\[\]\.]+)\]|\.([^\[\]\.]+)|^([^\[\]\.]+)|\./g, i = {
                            get: function () {
                                return t
                            },
                            set: function (e) {
                                t[""] = void 0 === t[""] ? e : [t[""], e]
                            },
                            build: function () {
                                return t
                            },
                            append: function (e) {
                                return new a(i, e)
                            }
                        }, o = null; o = r.exec(e);)
                        if (null != o[1])
                            i = i.append(parseInt(o[1]) || 0);
                        else {
                            var s = o[2] || o[3] || o[4];
                            if (null == s)
                                return t[e] = n,
                                    t;
                            i = i.append(s)
                        }
                    return i.set(n),
                        i.build()
                }

                function a(e, n) {
                    this.ref = e,
                        this.name = n,
                        this.build = this.ref.build,
                        this.get = function () {
                            var e = this.ref.get();
                            return null == e ? null : e[this.name]
                        },
                        this.set = function (e) {
                            var t = this.ref.get();
                            null == t && ("number" == typeof this.name ? this.ref.set(t = []) : this.ref.set(t = {})),
                                void 0 !== t[n] ? t[n] = [t[n], e] : t[n] = e
                        },
                        this.append = function (e) {
                            return this.next = new a(this, e)
                        }
                }
            }

            function d(e) {
                if (null == e || 0 === Object.keys(e).length)
                    return "";
                var a = [];
                return function (e, t) {
                        switch (u(e)) {
                            case "undefined":
                                break;
                            case "boolean":
                                a.push(t + "=" + e);
                                break;
                            case "string":
                                null == t || "" === t ? a.push(encodeURIComponent(e)) : a.push(t + "=" + encodeURIComponent(e));
                                break;
                            case "number":
                                a.push(t + "=" + e);
                                break;
                            case "object":
                                if (e instanceof Array) {
                                    for (var n = 0; n < e.length; n++)
                                        arguments.callee(e[n] || "", 0 < t.length ? t + "%5B" + (n || "") + "%5D" : "");
                                    return
                                }
                                if (null !== e) {
                                    var r = Object.keys(e);
                                    if (0 < r.length)
                                        for (n = 0; n < r.length; n++) {
                                            var i = encodeURIComponent(r[n]);
                                            null == i && (i = ""),
                                                0 != t.length && (i = t + "%5B" + i + "%5D");
                                            var o = e[r[n]];
                                            null == o && (o = ""),
                                                arguments.callee(o, i)
                                        }
                                    else if (e instanceof Date)
                                        var s = e.getFullYear() + "-" + ("0" + (s.getMonth() + 1)).slice(-2) + "-" + ("0" + e.getDate()).slice(-2) + " " + ("0" + e.getHours()).slice(-2) + "%3A" + ("0" + e.getMinutes()).slice(-2) + "%3A" + ("0" + e.getSeconds()).slice(-2);
                                    else
                                        arguments.callee(e.toString(), t)
                                }
                                break;
                            case "function":
                                arguments.callee(e(), t)
                        }
                    }(e, ""),
                    a.join("&")
            }
            var m = new Object;

            function g(e) {
                if (arguments[1] !== m)
                    return new g(e, m);
                e = l(e || c.location.href);
                var t = null,
                    n = null,
                    r = null,
                    i = null,
                    o = null;
                if (0 < e.length) {
                    var s = /^([^:/]+:\/\/|\/\/)/.exec(e) || "";
                    if (s && 0 < s.length) {
                        if (t = s[0],
                            e = e.substr(t.length),
                            -1 == (n = e.substr(0, f(e, ["/", "\\", "?", "#"])).replace(/[\/\\]$/g, "")).indexOf("."))
                            throw new Error('The "url" argument is invalid. because "domian" doesn\'t exist. from string : "' + e + '"');
                        e = e.substr(n.length)
                    }
                    r = e.substr(0, f(e, ["?", "#"])).replace(/[?#]$/g, ""),
                        e = e.substr(r.length),
                        r = r.replace(/(\\|\/)+/g, "/"),
                        i = e.substr(0, f(e, ["#"])),
                        e = e.substr(i.length),
                        o = e
                }
                this.params = p(i);
                var a = this;
                if ("function" == typeof Object.defineProperties) {
                    var u = function (e, t) {
                        throw new Error('The "' + e + '" format is invalid. from string : "' + t + '"')
                    };
                    Object.defineProperties(this, {
                        scheme: {
                            get: function () {
                                return t
                            },
                            set: function (e) {
                                e = l(e),
                                    !1 === /^([a-z]+:)?\/\/$/.test(e) && u("scheme", e),
                                    t = e
                            }
                        },
                        domain: {
                            get: function () {
                                return n
                            },
                            set: function (e) {
                                e = l(e),
                                    !1 === /^([a-z0-9]([a-z0-9\-]+[a-z0-9])?\.)+[a-z0-9]+\/?$/.test(e) && u("domain", e),
                                    "/" === e.slice(-1) && (e = e.slice(0, -1)),
                                    n = e
                            }
                        },
                        path: {
                            get: function () {
                                var e = r;
                                return null == t || "" === t || null == n || "" !== n || "/" !== (e = h(e)).charAt(0) && (e = "/" + e),
                                    e
                            },
                            set: function (e) {
                                e = l(e).replace(/([^\/]|^)[\/]{2,}/g, function (e) {
                                        return ":" === e.charAt(0) ? "://" : e.charAt(0) + "/"
                                    }),
                                    !1 === /^\/?(([^\/?#]+)(\/|$))+$/.test(e) && u("path", e),
                                    r = e
                            }
                        },
                        query: {
                            get: function () {
                                var e = d(a.params);
                                return "" === e ? "" : "?" + e
                            },
                            set: function (e) {
                                a.params = p(e)
                            }
                        },
                        anchor: {
                            get: function () {
                                return "" === o || "#" === o.charAt(0) ? o : "#" + o
                            },
                            set: function (e) {
                                o = l(e)
                            }
                        }
                    })
                } else
                    this.scheme = t,
                    this.domain = n,
                    this.path = r,
                    this.query = i,
                    this.anchor = o;
                this.toString = function () {
                    var e = this.path;
                    return null != t && "" !== t && null != n && "" === n || "/" !== (e = h(e)).charAt(0) && (e = "/" + e),
                        [this.scheme, this.domain, e, this.query, "#" === this.anchor ? "" : this.anchor].join("")
                }
            }

            function i(e, t) {
                if (null == e || 0 === e.length)
                    return t && new g(t).toString();
                if (null == t || 0 === t.length)
                    return new g(e).toString();
                /^\.\.[^/]/.test(t) && (t = "./" + t);
                var n = new g(e),
                    r = new g(t);
                return null != r.scheme ? ("//" === r.scheme && null != n.scheme && (r.scheme = n.scheme),
                    r.toString()) : (null != r.path && 0 < r.path.length && ("/" === r.path.charAt(0) ? n.path = r.path : "./" === r.path.substr(0, 2) ? n.path = [n.path, r.path.substr("/" === n.path.slice(-1) ? 2 : 1)].join("") : "/" === n.path.slice(-1) ? n.path = [n.path, r.path].join("") : "." !== r.path.charAt(0) && (n.path = [n.path.substr(0, n.path.lastIndexOf("/")), "/", r.path].join(""))),
                    null == r.query || 0 === r.query.length ? null != r.anchor && 0 < r.anchor.length ? n.anchor = r.anchor : n.query = "" : ("?&" === r.query.substr(0, 2) ? 2 < r.query.length && (null == n.query || 0 === n.query.length ? n.query = ["?", r.query.substr(2)] : n.query = [n.query, r.query.substr("&" === n.query.slice(-1) ? 2 : 1)].join("")) : n.query = r.query,
                        null != r.anchor && 0 < r.anchor.length && (n.anchor = r.anchor)),
                    n.toString())
            }
            g.encoded = d,
                g.combine = function (e, t) {
                    if (arguments.length < 2)
                        return e;
                    for (var n = e, r = 1; r < arguments.length; r++)
                        n = i(n, arguments[r]).toString();
                    return n
                },
                g.parseSearch = p,
                c[e] = g,
                "function" == typeof c.define && c.define(e, [], function () {
                    return g
                })
        }(window, "Url")
    },
    27: function (e, t, n) {},
    5: function (r, i, o) {
        var s, a;
        ! function (e) {
            if (void 0 === (a = "function" == typeof (s = e) ? s.call(i, o, i, r) : s) || (r.exports = a),
                !0,
                r.exports = e(),
                !!0) {
                var t = window.Cookies,
                    n = window.Cookies = e();
                n.noConflict = function () {
                    return window.Cookies = t,
                        n
                }
            }
        }(function () {
            function m() {
                for (var e = 0, t = {}; e < arguments.length; e++) {
                    var n = arguments[e];
                    for (var r in n)
                        t[r] = n[r]
                }
                return t
            }
            return function e(p) {
                function d(e, t, n) {
                    var r;
                    if ("undefined" != typeof document) {
                        if (1 < arguments.length) {
                            if ("number" == typeof (n = m({
                                    path: "/"
                                }, d.defaults, n)).expires) {
                                var i = new Date;
                                i.setMilliseconds(i.getMilliseconds() + 864e5 * n.expires),
                                    n.expires = i
                            }
                            n.expires = n.expires ? n.expires.toUTCString() : "";
                            try {
                                r = JSON.stringify(t),
                                    /^[\{\[]/.test(r) && (t = r)
                            } catch (e) {}
                            t = p.write ? p.write(t, e) : encodeURIComponent(String(t)).replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent),
                                e = (e = (e = encodeURIComponent(String(e))).replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent)).replace(/[\(\)]/g, escape);
                            var o = "";
                            for (var s in n)
                                n[s] && (o += "; " + s,
                                    !0 !== n[s] && (o += "=" + n[s]));
                            return document.cookie = e + "=" + t + o
                        }
                        e || (r = {});
                        for (var a = document.cookie ? document.cookie.split("; ") : [], u = /(%[0-9A-Z]{2})+/g, c = 0; c < a.length; c++) {
                            var l = a[c].split("="),
                                f = l.slice(1).join("=");
                            this.json || '"' !== f.charAt(0) || (f = f.slice(1, -1));
                            try {
                                var h = l[0].replace(u, decodeURIComponent);
                                if (f = p.read ? p.read(f, h) : p(f, h) || f.replace(u, decodeURIComponent),
                                    this.json)
                                    try {
                                        f = JSON.parse(f)
                                    } catch (e) {}
                                if (e === h) {
                                    r = f;
                                    break
                                }
                                e || (r[h] = f)
                            } catch (e) {}
                        }
                        return r
                    }
                }
                return (d.set = d).get = function (e) {
                        return d.call(d, e)
                    },
                    d.getJSON = function () {
                        return d.apply({
                            json: !0
                        }, [].slice.call(arguments))
                    },
                    d.defaults = {},
                    d.remove = function (e, t) {
                        d(e, "", m(t, {
                            expires: -1
                        }))
                    },
                    d.withConverter = e,
                    d
            }(function () {})
        })
    },
    9: function (e, t) {
        e.exports = function (e, t) {
            for (var n = document.querySelectorAll(".simpleTips"), r = 0; r < n.length; r++) {
                var i = n[r];
                i.parentNode && i.parentNode.removeChild(i)
            }
            t = +t || 1500;
            var o = document.createElement("div");
            return o.className = "simpleTips",
                o.setAttribute("style", "width:200px;line-height:36px;padding:8px 0; font-size:14px; color:#fff; text-align:center; background:rgba(0,0,0,.5); position:fixed; left:50%; margin-left:-100px; top:50%; margin-top:-32px; z-index:999999999999999999999; -webkit-border-radius:5px;-moz-border-radius:5px;-ms-border-radius:5px;border-radius:5px;"),
                o.innerHTML = e,
                document.body.appendChild(o),
                setTimeout(function () {
                    o.parentNode && o.parentNode.removeChild(o)
                }, t),
                o
        }
    }
});
