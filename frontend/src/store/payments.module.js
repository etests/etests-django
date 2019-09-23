import { paymentService } from "@/api/payment.service";

const initialState = {
  status: {}
};

export const payments = {
  namespaced: true,
  state: initialState,
  actions: {
    create({ dispatch, commit }, data) {
      commit("createRequest");
      paymentService.create(data).then(
        data => {
          commit("createSuccess");
          dispatch("alert/success", "Payment details received successfully", {
            root: true
          });
        },
        error => {
          commit("createFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    }
  },
  mutations: {
    createSuccess(state) {
      state.status = { created: true };
    },
    createRequest(state) {
      state.status = { creating: true };
    },
    createFailure(state, error) {
      state.status = { error: error };
    }
  }
};
