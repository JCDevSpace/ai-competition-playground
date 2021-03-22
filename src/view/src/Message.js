const MsgType = {
  OBSERVE : "observe",
  SIGNUP : "signup",
  T_START : "t-start",
  T_PROGRESS : "t-progress",
  T_END : "t-end",
  PLAYING_AS : "playing-as",
  T_ACTION : "t-action",
  G_START : "g-start",
  G_ACTION : "g-action",
  G_KICK : "g-kick",
  INVALID : "invalid"
};

const value2type = (v) => {
  for (const [key, value] of Object.entries(MsgType)) {
    if (value === v)
      return key;
  }
  return MsgType.INVALID;
}

const valid_type = (type) => {
  return type !== MsgType.INVALID;
}

const str_converter = (value) => {
  return value;
}

const list_converter = (value) => {
  return value;
}

const list2d_converter = (value) => {
  return value;
}

const action_converter = (value) => {
  return value;
}

const state_converter = (value) => {
  return value;
}

const CONVERTERS = {
  OBSERVE: str_converter,
  SIGNUP: str_converter,
  PLAYING_AS: str_converter,
  G_KICK: str_converter,
  T_START: list_converter,
  T_END: list_converter,
  T_PROGRESS: list2d_converter,
  G_ACTION: action_converter,
  G_START: state_converter,
  T_ACTION: state_converter
};

const decode = (message) => {
  let content = null;
  let msg_type = null;
  try {
    const msg = JSON.parse(message);
    msg_type = value2type(msg["msg-type"])

    if (valid_type(msg_type)) {
      const converter = CONVERTERS[msg_type];
      const ret = converter(msg["content"]);
      if (ret)
        content = ret;
      else
        msg_type = MsgType.INVALID;
    }
  } catch (error) {
    console.log(error, "while decoding message")
    msg_type = MsgType.INVALID;
  }
  return {msg_type: msg_type, content: content};
}

export { decode, valid_type };