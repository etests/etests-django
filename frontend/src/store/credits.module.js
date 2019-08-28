import { creditService } from "@/api/credit.service";

const initialState = {
  status: {},
  credits: null
};

export const credits = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }) {
      commit("getRequest");
      creditService.get().then(
        credits => {
          commit("getSuccess", credits);
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
    getSuccess(state, credits) {
      state.status = { exists: true };
      state.credits = credits;
    },
    getFailure(state, error) {
      state.status = { error };
    }
  }
};
