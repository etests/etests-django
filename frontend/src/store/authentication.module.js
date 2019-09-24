import { userService } from "@/api/user.service";

const user = JSON.parse(localStorage.getItem("user"));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: {}, user: { type: "student" } };

export const authentication = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ dispatch, commit }, { username, password }) {
      commit("loginRequest", { name: username });

      userService.login(username, password).then(
        data => {
          commit("loginSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", `Welcome ${data.user.name}!`, {
              root: true
            });
          });
        },
        error => {
          commit("loginFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    refresh({ commit }) {
      commit("refreshRequest");

      userService.refresh().then(
        data => {
          commit("refreshSuccess", data);
        },
        error => {
          commit("refreshFailure", error);
        }
      );
    },
    register({ dispatch, commit }, data) {
      commit("registerRequest", data);
      const credentials = {
        username: data.email || data.phone,
        password: data.password
      };

      userService.register(data).then(
        data => {
          commit("registerSuccess", data);
          setTimeout(() => {
            dispatch("login", credentials);
          });
        },
        error => {
          commit("registerFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    logout({ dispatch, commit }) {
      userService.logout();
      commit("logout");
      setTimeout(() => {
        dispatch("alert/success", "See you soon!", {
          root: true
        });
      });
    }
  },
  mutations: {
    loginRequest(state, user) {
      state.status = { loggingIn: true };
    },
    loginSuccess(state, data) {
      state.status = { loggedIn: true };
      state.user = data.user;
    },
    loginFailure(state, error) {
      state.status = { error };
    },
    refreshRequest(state) {
      state.status.refreshing = true;
    },
    refreshSuccess(state) {
      state.status = { loggedIn: true };
    },
    refreshFailure(state, error) {
      state.status.error = error;
      this.dispatch("logout");
    },
    logout(state) {
      state.status = {};
      state.user = { type: "student" };
    },
    registerRequest(state, user) {
      state.status = { registering: true };
    },
    registerSuccess(state, user) {
      state.status = {};
      state.user = user;
    },
    registerFailure(state, error) {
      state.status = {};
    }
  }
};
