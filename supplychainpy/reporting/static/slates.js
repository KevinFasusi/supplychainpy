/**
 * Created by Fasusi on 14/07/2016.
 */
"use strict";
var React = require('react');

export class PlainSlate extends React.Component{
    constructor(id_tag, html_template, location, css_style) {
        this.id_tag = id_tag;
        this.html_template = html_template;
        this.location = location;
        this.css_style = css_style;
    }

    load_slate() {

        $(this.id_tag).append().html(this.html_template)
            .find(this.location).css(this.css_style);

    }

}


export class IndicatorSlate extends PlainSlate {
    constructor(icon) {
        super();
        this.icon = icon;
    }

}