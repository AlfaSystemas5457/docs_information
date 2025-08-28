/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { url } from "@web/core/utils/urls";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { FileUploader } from "@web/views/fields/file_handler";

import { Component, onWillUpdateProps, useState } from "@odoo/owl";

export class FileViewerField extends Component {
    static template = "docs_information.FileViewerField";
    static components = { FileUploader };
    static props = { ...standardFieldProps };

    setup() {
        this.notification = useService("notification");
        this.state = useState({
            isValid: true,
            objectUrl: "",
            fileType: "",
        });

        onWillUpdateProps((nextProps) => {
            if (nextProps.readonly) {
                this.state.objectUrl = "";
                this.state.fileType = "";
            }
        });
    }

    get url() {
        if (!this.state.isValid || !this.props.record.data[this.props.name]) {
            return null;
        }

        const file_extension_current = this.props.record.data.file_extension

        if (file_extension_current && file_extension_current == 'pdf') {
            const page = this.props.record.data[`${this.props.name}_page`] || 1;
            const file = encodeURIComponent(
                this.state.objectUrl ||
                url("/web/content", {
                    model: this.props.record.resModel,
                    field: this.props.name,
                    id: this.props.record.resId,
                })
            );
            return `/web/static/lib/pdfjs/web/viewer.html?file=${file}#page=${page}`;
        }

        const img_extensions = ["png", "jpg", "jpeg"];

        if (file_extension_current && img_extensions.includes(file_extension_current.toLowerCase())) {
            return this.state.objectUrl ||
                url("/web/image", {
                    model: this.props.record.resModel,
                    id: this.props.record.resId,
                    field: this.props.name,
                });
        }
    }

    update({ data }) {
        const changes = {
            [this.props.name]: data || false,
            filename: data ? this.props.record.data.filename : false,
        };
        return this.props.record.update(changes);
    }

    onFileRemove() {
        this.state.isValid = true;
        this.props.record.update({
            [this.props.name]: false,
            filename: false
        });
    }

    onFileUploaded(payload) {
        const { data, objectUrl, name } = payload;

        const fileType = (name ? name.split('.') : [""]).pop().toLowerCase();
        this.state.isValid = true;
        this.state.objectUrl = objectUrl;
        this.state.fileType = fileType;
        this.props.record.update({
            [this.props.name]: data,
            filename: name
        });
    }

    onLoadFailed() {
        this.state.isValid = false;
        this.notification.add(this.env._t("Could not display the selected file"), { type: "danger" });
    }
}

export const fileViewerField = {
    component: FileViewerField,
    displayName: _t("File Viewer"),
    supportedOptions: [{
        label: _t("Preview image"),
        name: "preview_image",
        type: "field",
        availableTypes: ["binary"],
    }],
    supportedTypes: ["binary"],
};

registry.category("fields").add("file_viewer", fileViewerField);
