/**
 * Created by Fasusi on 14/07/2016.
 */
"use strict";

class PlainSlate {
    constructor(id_tag, html_template, location, css_style) {
        this.id_tag = id_tag;
        this.html_template = html_template;
        this.location = location;
        this.css_style = css_style;
    }


}


class IndicatorSlate extends PlainSlate {
    constructor(icon) {
        super();
        this.icon = icon;
    }

}