from pathlib import Path
from typing import get_type_hints, _GenericAlias
from functools import singledispatch, update_wrapper

def funcdispatch(method: bool = True):
    """
    メソッド用のオーバーロード実装
    Args:
        method: メソッドかどうか
    """

    def dispach(func):
        # 通常のsingledispatchを取得
        dispatcher = singledispatch(func)

        # regist関数リスト
        funclist = [func]

        def register(cls, func=None):
            """
            registerのオーバーライド
            registされる関数を保持しておく
            """
            # typingの型ではsingledispatchのregister時にtypeと判定されずエラーになる
            # funcがNoneの際にエラーになるので，予めclsとfuncを取得して変換する
            clses = [cls]
            if func is None:
                ann = getattr(cls, '__annotations__', {})
                if ann:
                    func = cls
                    _, cls = next(iter(get_type_hints(func).items()))

                    clses = []
                    if isinstance(cls, _GenericAlias):
                        clses.extend(cls.__args__)
                    else:
                        clses.append(cls)
            # 関数登録
            for cls in clses:
                func = dispatcher.register(cls, func)   # singledispatchのregisterを呼んでおく
            funclist.append(func)
            return func

        def wrapper(*args, **kwargs):
            """
            ラップ
            registした関数から一致する型を見つける
            """
            # デフォルトは第1引数
            # インスタンスメソッドの場合はseldになる
            dispatch_class = args[0].__class__

            # キーワード引数のみで指定されている場合は，registされた関数からクラスを取得
            args_is_none = (not method and len(args) == 0) or (method and len(args) == 1)
            if args_is_none and len(kwargs.keys()) > 0:
                for func in funclist:
                    # 型ヒントから第2引数名を取得して，キーワード引数から値を取得
                    # selfには型ヒントが付いていない想定なので第2引数
                    argname, _ = next(iter(get_type_hints(func).items()))

                    # 値が存在しない場合は、次の関数を探索
                    if not argname in kwargs:
                        continue

                    # 値のクラスを取得
                    arg = kwargs.get(argname, None)
                    dispatch_class = arg.__class__
                    break

            # 通常の引数が指定されている場合は，メソッド種類に従い処理
            else:
                # インスタンスメソッドの場合は第2引数を取得
                if method:
                    dispatch_class = args[1].__class__

                # 派生クラスでは判定できないので、Pathは基底クラスに変換
                if issubclass(dispatch_class, Path):
                    dispatch_class = Path

            return dispatcher.dispatch(dispatch_class)(*args, **kwargs)

        wrapper.register = register
        update_wrapper(wrapper, func)
        return wrapper
    return dispach