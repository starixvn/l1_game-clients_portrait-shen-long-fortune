import Observer from "observer";

import { _decorator, Component, macro, sp } from "cc";
import { AnimationUtils } from "db://shared-components/shared/utils";
import "./../../../resources/i18n";

const { ccclass, property } = _decorator;
const { observer, render, handle } = Observer;

@ccclass
export class DecorFire extends Component {
    @property(sp.Skeleton)
    nodeFire1: sp.Skeleton = null;

    @property(sp.Skeleton)
    nodeFire2: sp.Skeleton = null;

    onLoad() {
        this.schedule(
            () => {
                this.playAnimationFire(this.nodeFire1, "iron-torch");
            },
            5,
            macro.REPEAT_FOREVER,
            0
        );

        this.schedule(
            () => {
                this.playAnimationFire(this.nodeFire2, "iron-torch");
            },
            5,
            macro.REPEAT_FOREVER,
            2
        );
    }

    playAnimationFire(spine: sp.Skeleton, anim: string) {
        AnimationUtils.playSpine(spine, anim, false);
    }
}
