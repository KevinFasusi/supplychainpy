Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var PlainSlate = exports.PlainSlate = function () {
    function PlainSlate(id_tag, html_template, location, css_style) {
        _classCallCheck(this, PlainSlate);

        this.id_tag = id_tag;
        this.html_template = html_template;
        this.location = location;
        this.css_style = css_style;
    }

    _createClass(PlainSlate, [{
        key: "load_slate",
        value: function load_slate() {

            $(this.id_tag).append().html(this.html_template).find(this.location).css(this.css_style);
        }
    }]);

    return PlainSlate;
}();

var IndicatorSlate = exports.IndicatorSlate = function (_PlainSlate) {
    _inherits(IndicatorSlate, _PlainSlate);

    function IndicatorSlate(icon) {
        _classCallCheck(this, IndicatorSlate);

        var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(IndicatorSlate).call(this));

        _this.icon = icon;
        return _this;
    }

    return IndicatorSlate;
}(PlainSlate);

//# sourceMappingURL=slates-compiled.js.map