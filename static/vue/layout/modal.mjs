const template = `
<div class="modal fade" role="dialog" :id="modal_id">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header" :class="headerBgClass">
                <h5 class="modal-title">{{ title }}</h5>
            </div>
            <div class="modal-body bg-dark">
                <slot></slot>
            </div>
        </div>
    </div>
</div>
`


export const Modal = {
    name: "Modal",
    props: {
        modal_id: String,
        title: String,
        header_bg: String,
        footer: Boolean,
    },
    computed: {
        headerBgClass() {
            return "bg-" + this.header_bg;
        }
    },
    template: template
}