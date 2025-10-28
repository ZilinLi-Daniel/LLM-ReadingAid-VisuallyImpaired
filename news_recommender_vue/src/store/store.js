import { reactive } from "vue";

export const store = reactive({
  version: "en",
  change() {
    this.version = this.version === "en" ? "zh" : "en";
  },
});
