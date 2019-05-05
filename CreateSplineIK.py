import bpy
C = bpy.context
D = bpy.data

bz = []

curve = C.active_object

#1:カーブからスプライン座標を取得
for vec in curve.data.splines[0].bezier_points:
    bz.append(vec.co)
print(bz)

#2:アーマチュア作成
bpy.ops.object.add(type='ARMATURE', enter_editmode=True, location=(0,0,0))
amt = C.active_object

#3:Rootボーン作成
bRoot = amt.data.edit_bones.new("Root_Bone")
b0 = bRoot
b0.head = (0,0,0)
b0.tail = (0,0,1)
b0.use_deform = False

#4:スプライン要素分だけハンドルボーン作成(Rootボーンを親)
hb_names = []
for i in bz:
    b1 = amt.data.edit_bones.new("CTL_Bone")
    b1.head = i
    b1.tail = (b1.head.x, b1.head.y, b1.head.z + 1)
    b1.use_deform = False
    b1.parent = bRoot
    hb_names.append(b1.name)
    b0 = b1

#5:適当な数分だけボーン作成
b0 = bRoot
for i in range(10):
    b1 = amt.data.edit_bones.new("Bone")
    b1.head = b0.tail
    b1.tail = (0, 0, b1.head.z + 1)
    b1.use_deform = True
    b1.use_connect = True
    b1.parent = b0
    b0 = b1
setName = b0.name

#6:スプラインIKの設定
bpy.ops.object.mode_set(mode='POSE')
spIK = amt.pose.bones[setName].constraints.new("SPLINE_IK")
spIK.target = curve
spIK.chain_count = 10

#7:各スプライン要素とハンドルボーンをフック
count = 0
for hbn in hb_names:
    bpy.ops.object.mode_set(mode='OBJECT')
    hook = curve.modifiers.new("HOOK", "HOOK")
    hook.object = amt
    hook.subtarget = hbn
    hookName = hook.name
    C.scene.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    for tmpP in curve.data.splines[0].bezier_points:
        tmpP.select_control_point = False
    p = curve.data.splines[0].bezier_points[count]
    count = count + 1
    p.select_control_point = True
    print(hookName)
    bpy.ops.object.hook_assign(modifier = hookName)
    bpy.ops.object.hook_reset(modifier = hookName)
bpy.ops.object.mode_set(mode='OBJECT')
