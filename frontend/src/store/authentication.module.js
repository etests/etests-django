import { userService } from "@/api/user.service";
import router from "@/router";

const auth = JSON.parse(localStorage.getItem("auth"));
const initialState = auth
  ? { status: { loggedIn: true }, auth }
  : { status: {}, auth: null };

export const authentication = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ dispatch, commit }, { username, password }) {
      commit("loginRequest", { username });

      userService.login(username, password).then(
        auth => {
          commit("loginSuccess", auth);
          router.push("/");
        },
        error => {
          commit("loginFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    logout({ commit }) {
      userService.logout();
      commit("logout");
    }
  },
  mutations: {
    loginRequest(state, auth) {
      state.status = { loggingIn: true };
      state.auth = auth;
    },
    loginSuccess(state, auth) {
      state.status = { loggedIn: true };
      state.auth = auth;
    },
    loginFailure(state) {
      state.status = {};
      state.auth = null;
    },
    logout(state) {
      state.status = {};
      state.auth = null;
    }
  }
};
