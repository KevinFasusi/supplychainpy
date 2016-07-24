function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var PlainSlate = function PlainSlate(id_tag, html_template, location, css_style) {
    _classCallCheck(this, PlainSlate);

    this.id_tag = id_tag;
    this.html_template = html_template;
    this.location = location;
    this.css_style = css_style;
};

var IndicatorSlate = function (_PlainSlate) {
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