/** @odoo-module */
import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {useService} from "@web/core/utils/hooks"
import {FormView} from "@app_one/components/formView/formVeiw"
export class ListViewActions extends Component {
    static template = "app_one.listView";
    static components = {FormView}
    setup(){

       this.state = useState({
       "records": []
       });
    this.orm = useService("orm")
    this.rpc = useService("rpc")
    this.loadRecords();

console.log(this.env.services);
    this.intervalId = setInterval(() => {
         this.loadRecords();
    },3000)
    onWillUnmount(() => {clearInterval(this.intervalId)})

    };
//    async loadRecords() {
//       const result = await this.orm.searchRead("property", [], [])
//       console.log(result)
//        this.state.records = result;
//}
            async loadRecords() {
            const result = await this.rpc("/web/dataset/call_kw/", {
            model : "property",
            method: "search_read",
            args: [[]],
            kwargs: {fields: ["id", "name", "postcode"]},
            })
            console.log(result);
            this.state.records = result;
            }
            async createRecord() {
                await this.rpc("/web/dataset/call_kw/", {
                model:"property",
                method: "create",
                args: [{
                name: "new Name",
                postcode: "12235",
                date_availability: "2025-05-02"}],
                kwargs: {}
                })
                this.loadRecords();

            }

              async deleteRecord(recordId) {
                    await this.rpc("/web/dataset/call_kw/", {
                        model:"property",
                        method: "unlink",
                        args:[[recordId]],
                          kwargs: {}
                    })
                this.loadRecords();
              }

              toggleCreateForm() {
              console.log("done")
                this.state.showCreateForm = !this.state.showCreateForm;
              }
              onRecordCreated = () => {
                this.loadRecords();
                this.state.showCreateForm = false;


              }

}

registry.category("actions").add("app_one.action_list_view", ListViewActions);
