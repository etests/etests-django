import { TransactionsService } from "@/api/transaction.service";

const initialState = {
  status: {},
  items: null
};

export const transactions = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }) {
      commit("getRequest");
      TransactionsService.get().then(
        transactions => {
          commit("getSuccess", transactions);
        },
        error => {
          commit("getFailure", error);
        }
      );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, transactions) {
      state.status = { exists: true };
      state.items = transactions;
    },
    getFailure(state, error) {
      state.status = { error };
    }
  }
};
