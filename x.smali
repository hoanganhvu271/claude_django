.method private final isFaceOutSide(Landroid/graphics/RectF;Landroid/graphics/RectF;)Z
    .locals 2

    iget-object v0, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugFace:Lkotlinx/coroutines/flow/StateFlow;

    invoke-static {p1}, Lkotlin/collections/CollectionsKt;->listOf(Ljava/lang/Object;)Ljava/util/List;

    move-result-object v1

    invoke-virtual {p0, v0, v1}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    invoke-virtual {p2, p1}, Landroid/graphics/RectF;->contains(Landroid/graphics/RectF;)Z

    move-result p1

    xor-int/lit8 p1, p1, 0x1

    return p1
.end method

.method private final isChinOutSide(Landroid/graphics/RectF;Landroid/graphics/RectF;)Z
    .locals 4

    iget-object v0, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugFace:Lkotlinx/coroutines/flow/StateFlow;

    const/4 v1, 0x2

    new-array v2, v1, [Landroid/graphics/RectF;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    const/4 v3, 0x1

    aput-object p2, v2, v3

    invoke-static {v2}, Lkotlin/collections/CollectionsKt;->listOf([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v2

    invoke-virtual {p0, v0, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget v0, p1, Landroid/graphics/RectF;->left:F

    iget v2, p1, Landroid/graphics/RectF;->right:F

    add-float/2addr v0, v2

    int-to-float v1, v1

    div-float/2addr v0, v1

    iget p1, p1, Landroid/graphics/RectF;->bottom:F

    invoke-virtual {p2, v0, p1}, Landroid/graphics/RectF;->contains(FF)Z

    move-result p1

    xor-int/2addr p1, v3

    return p1
.end method

.method private final processDetection(Lcom/otaliastudios/cameraview/frame/Frame;Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FaceDetectionConfig;Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings;Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$ProcessStep;)V
    .locals 18

    move-object/from16 v9, p0

    invoke-direct/range {p0 .. p0}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->getDetectionSkipFrame()Z

    move-result v0

    if-eqz v0, :cond_0

    return-void

    :cond_0
    const/4 v0, 0x1

    iput-boolean v0, v9, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->isProcessing:Z

    iget-object v1, v9, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugInfo:Lkotlinx/coroutines/flow/StateFlow;

    invoke-interface {v1}, Lkotlinx/coroutines/flow/StateFlow;->getValue()Ljava/lang/Object;

    move-result-object v2

    move-object v10, v2

    check-cast v10, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    invoke-virtual/range {p4 .. p4}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$ProcessStep;->toString()Ljava/lang/String;

    move-result-object v13

    const/4 v11, 0x0

    const/4 v12, 0x0

    const/4 v14, 0x0

    const/4 v15, 0x0

    const/16 v16, 0x1b

    const/16 v17, 0x0

    invoke-static/range {v10 .. v17}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;->copy$default(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;FFLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    move-result-object v2

    invoke-virtual {v9, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-boolean v1, v9, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->faceDetected:Z

    if-eqz v1, :cond_1

    iget-object v1, v9, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->processState:Lkotlinx/coroutines/flow/StateFlow;

    sget-object v2, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Nothing;->INSTANCE:Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Nothing;

    invoke-virtual {v9, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    :cond_1
    new-instance v5, Lkotlin/jvm/internal/Ref$ObjectRef;

    invoke-direct {v5}, Lkotlin/jvm/internal/Ref$ObjectRef;-><init>()V

    new-instance v7, Lkotlin/jvm/internal/Ref$LongRef;

    invoke-direct {v7}, Lkotlin/jvm/internal/Ref$LongRef;-><init>()V

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v1

    invoke-virtual/range {p2 .. p2}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FaceDetectionConfig;->getCameraSide()Lcom/trustingsocial/tvcoresdk/external/CameraSide;

    move-result-object v3

    sget-object v4, Lcom/trustingsocial/tvcoresdk/external/CameraSide;->FRONT:Lcom/trustingsocial/tvcoresdk/external/CameraSide;

    if-ne v3, v4, :cond_2

    goto :goto_0

    :cond_2
    const/4 v0, 0x0

    :goto_0
    const/16 v3, 0x5a

    const/16 v4, 0x280

    move-object/from16 v6, p1

    invoke-static {v6, v0, v3, v4}, Lcom/trustingsocial/tvcoresdk/internal/extension/e;->a(Lcom/otaliastudios/cameraview/frame/Frame;ZII)Landroid/graphics/Bitmap;

    move-result-object v0

    iput-object v0, v5, Lkotlin/jvm/internal/Ref$ObjectRef;->element:Ljava/lang/Object;

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v3

    sub-long/2addr v3, v1

    iput-wide v3, v7, Lkotlin/jvm/internal/Ref$LongRef;->element:J

    sget-object v0, Lcom/trustingsocial/tvcoresdk/external/TVGraphicsUtils;->INSTANCE:Lcom/trustingsocial/tvcoresdk/external/TVGraphicsUtils;

    iget-object v1, v5, Lkotlin/jvm/internal/Ref$ObjectRef;->element:Ljava/lang/Object;

    check-cast v1, Landroid/graphics/Bitmap;

    invoke-virtual {v0, v1}, Lcom/trustingsocial/tvcoresdk/external/TVGraphicsUtils;->squareUp(Landroid/graphics/Bitmap;)Landroid/graphics/Bitmap;

    move-result-object v2

    invoke-static/range {p0 .. p0}, Landroidx/lifecycle/ViewModelKt;->getViewModelScope(Landroidx/lifecycle/ViewModel;)Lkotlinx/coroutines/CoroutineScope;

    move-result-object v10

    new-instance v13, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processDetection$1;

    const/4 v8, 0x0

    move-object v0, v13

    move-object/from16 v1, p0

    move-object/from16 v3, p2

    move-object/from16 v4, p3

    move-object/from16 v6, p4

    invoke-direct/range {v0 .. v8}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processDetection$1;-><init>(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;Landroid/graphics/Bitmap;Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FaceDetectionConfig;Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings;Lkotlin/jvm/internal/Ref$ObjectRef;Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$ProcessStep;Lkotlin/jvm/internal/Ref$LongRef;Lkotlin/coroutines/Continuation;)V

    const/4 v11, 0x0

    const/4 v12, 0x0

    const/4 v14, 0x3

    const/4 v15, 0x0

    invoke-static/range {v10 .. v15}, Lkotlinx/coroutines/BuildersKt;->launch$default(Lkotlinx/coroutines/CoroutineScope;Lkotlin/coroutines/CoroutineContext;Lkotlinx/coroutines/CoroutineStart;Lkotlin/jvm/functions/Function2;ILjava/lang/Object;)Lkotlinx/coroutines/Job;

    return-void
.end method

.method private final isNotFrontal([Landroid/graphics/PointF;)Z
    .locals 19

    move-object/from16 v0, p0

    const/4 v1, 0x0

    aget-object v2, p1, v1

    const/4 v3, 0x1

    aget-object v4, p1, v3

    const/4 v5, 0x2

    aget-object v6, p1, v5

    const/4 v7, 0x3

    aget-object v8, p1, v7

    const/4 v9, 0x4

    aget-object v10, p1, v9

    const/4 v11, 0x5

    aget-object v12, p1, v11

    iget v13, v2, Landroid/graphics/PointF;->y:F

    iget v14, v4, Landroid/graphics/PointF;->y:F

    add-float/2addr v13, v14

    const/high16 v14, 0x3f000000    # 0.5f

    mul-float/2addr v13, v14

    iget v15, v8, Landroid/graphics/PointF;->y:F

    sub-float v16, v13, v15

    const v17, 0x3fb33333    # 1.4f

    mul-float v16, v16, v17

    add-float v13, v16, v13

    iget v14, v6, Landroid/graphics/PointF;->y:F

    sub-float/2addr v14, v15

    const v16, 0x3f99999a    # 1.2f

    mul-float v14, v14, v16

    sub-float/2addr v15, v14

    const/4 v14, 0x6

    new-array v11, v14, [Ljava/lang/Float;

    iget v2, v2, Landroid/graphics/PointF;->x:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    aput-object v2, v11, v1

    iget v2, v4, Landroid/graphics/PointF;->x:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    aput-object v2, v11, v3

    iget v2, v6, Landroid/graphics/PointF;->x:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    aput-object v2, v11, v5

    iget v2, v8, Landroid/graphics/PointF;->x:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    aput-object v2, v11, v7

    iget v2, v10, Landroid/graphics/PointF;->x:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    aput-object v2, v11, v9

    iget v2, v12, Landroid/graphics/PointF;->x:F

    invoke-static {v2}, Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;

    move-result-object v2

    const/4 v4, 0x5

    aput-object v2, v11, v4

    invoke-static {v11, v14}, Ljava/util/Arrays;->copyOf([Ljava/lang/Object;I)[Ljava/lang/Object;

    move-result-object v2

    invoke-static {v2}, Lkotlin/collections/CollectionsKt;->listOf([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v2

    invoke-static {v2}, Ljava/util/Collections;->min(Ljava/util/Collection;)Ljava/lang/Object;

    move-result-object v2

    const-string v4, "min(listOf(*xCoordinates))"

    invoke-static {v2, v4}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V

    check-cast v2, Ljava/lang/Number;

    invoke-virtual {v2}, Ljava/lang/Number;->floatValue()F

    move-result v2

    invoke-static {v13, v15}, Ljava/lang/Math;->min(FF)F

    move-result v4

    invoke-static {v11, v14}, Ljava/util/Arrays;->copyOf([Ljava/lang/Object;I)[Ljava/lang/Object;

    move-result-object v5

    invoke-static {v5}, Lkotlin/collections/CollectionsKt;->listOf([Ljava/lang/Object;)Ljava/util/List;

    move-result-object v5

    invoke-static {v5}, Ljava/util/Collections;->max(Ljava/util/Collection;)Ljava/lang/Object;

    move-result-object v5

    const-string v6, "max(listOf(*xCoordinates))"

    invoke-static {v5, v6}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V

    check-cast v5, Ljava/lang/Number;

    invoke-virtual {v5}, Ljava/lang/Number;->floatValue()F

    move-result v5

    invoke-static {v13, v15}, Ljava/lang/Math;->max(FF)F

    move-result v6

    iget v7, v8, Landroid/graphics/PointF;->x:F

    iget v9, v10, Landroid/graphics/PointF;->x:F

    sub-float/2addr v7, v9

    invoke-static {v7}, Ljava/lang/Math;->abs(F)F

    move-result v7

    iget v9, v8, Landroid/graphics/PointF;->x:F

    iget v11, v12, Landroid/graphics/PointF;->x:F

    sub-float/2addr v9, v11

    invoke-static {v9}, Ljava/lang/Math;->abs(F)F

    move-result v9

    div-float/2addr v7, v9

    iget v8, v8, Landroid/graphics/PointF;->x:F

    iget v9, v10, Landroid/graphics/PointF;->x:F

    sub-float v9, v8, v9

    const/4 v10, 0x0

    cmpg-float v11, v9, v10

    if-gez v11, :cond_0

    iget v11, v12, Landroid/graphics/PointF;->x:F

    sub-float/2addr v11, v8

    float-to-double v13, v11

    sub-float v11, v5, v2

    move/from16 v16, v4

    float-to-double v3, v11

    const-wide v17, 0x3fa999999999999aL    # 0.05

    mul-double v3, v3, v17

    cmpl-double v3, v13, v3

    if-lez v3, :cond_1

    const/4 v3, 0x1

    goto :goto_0

    :cond_0
    move/from16 v16, v4

    :cond_1
    move v3, v1

    :goto_0
    cmpl-float v4, v9, v10

    if-lez v4, :cond_2

    iget v4, v12, Landroid/graphics/PointF;->x:F

    sub-float/2addr v4, v8

    float-to-double v8, v4

    sub-float v4, v5, v2

    float-to-double v10, v4

    const-wide v12, -0x4056666666666666L    # -0.05

    mul-double/2addr v10, v12

    cmpg-double v4, v8, v10

    if-gez v4, :cond_2

    const/4 v4, 0x1

    goto :goto_1

    :cond_2
    move v4, v1

    :goto_1
    const/high16 v8, 0x3f000000    # 0.5f

    cmpg-float v9, v7, v8

    if-gez v9, :cond_3

    const/4 v9, 0x1

    goto :goto_2

    :cond_3
    move v9, v1

    :goto_2
    const/4 v10, 0x1

    int-to-float v11, v10

    div-float/2addr v11, v8

    cmpl-float v7, v7, v11

    if-lez v7, :cond_4

    const/4 v10, 0x1

    goto :goto_3

    :cond_4
    move v10, v1

    :goto_3
    const-string v7, "partial_face"

    if-eqz v4, :cond_5

    iget-object v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->uiState:Lkotlinx/coroutines/flow/StateFlow;

    new-instance v2, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Failure;

    invoke-direct {v2, v7}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Failure;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-object v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugInfo:Lkotlinx/coroutines/flow/StateFlow;

    invoke-interface {v1}, Lkotlinx/coroutines/flow/StateFlow;->getValue()Ljava/lang/Object;

    move-result-object v2

    move-object v3, v2

    check-cast v3, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    const/4 v4, 0x0

    const/4 v5, 0x0

    const/4 v6, 0x0

    const/4 v8, 0x0

    const/16 v9, 0x17

    const/4 v10, 0x0

    const-string v7, "partial_face"

    invoke-static/range {v3 .. v10}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;->copy$default(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;FFLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    move-result-object v2

    invoke-virtual {v0, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    const/4 v1, 0x1

    return v1

    :cond_5
    if-eqz v3, :cond_6

    iget-object v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->uiState:Lkotlinx/coroutines/flow/StateFlow;

    new-instance v2, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Failure;

    invoke-direct {v2, v7}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Failure;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-object v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugInfo:Lkotlinx/coroutines/flow/StateFlow;

    invoke-interface {v1}, Lkotlinx/coroutines/flow/StateFlow;->getValue()Ljava/lang/Object;

    move-result-object v2

    move-object v3, v2

    check-cast v3, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    const/4 v4, 0x0

    const/4 v5, 0x0

    const/4 v6, 0x0

    const/4 v8, 0x0

    const/16 v9, 0x17

    const/4 v10, 0x0

    const-string v7, "partial_face"

    invoke-static/range {v3 .. v10}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;->copy$default(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;FFLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    move-result-object v2

    invoke-virtual {v0, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    const/4 v1, 0x1

    return v1

    :cond_6
    if-nez v10, :cond_8

    if-eqz v9, :cond_7

    goto :goto_4

    :cond_7
    sub-float v3, v5, v2

    const v4, 0x3d4ccccd    # 0.05f

    mul-float/2addr v3, v4

    sub-float/2addr v2, v3

    add-float/2addr v5, v3

    new-instance v3, Landroid/graphics/RectF;

    move/from16 v4, v16

    invoke-direct {v3, v2, v4, v5, v6}, Landroid/graphics/RectF;-><init>(FFFF)V

    return v1

    :cond_8
    :goto_4
    iget-object v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->uiState:Lkotlinx/coroutines/flow/StateFlow;

    new-instance v2, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Failure;

    const-string v3, "not_frontal"

    invoke-direct {v2, v3}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$Failure;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-object v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugInfo:Lkotlinx/coroutines/flow/StateFlow;

    invoke-interface {v1}, Lkotlinx/coroutines/flow/StateFlow;->getValue()Ljava/lang/Object;

    move-result-object v2

    move-object v3, v2

    check-cast v3, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    const/4 v4, 0x0

    const/4 v5, 0x0

    const/4 v6, 0x0

    const/4 v8, 0x0

    const/16 v9, 0x17

    const/4 v10, 0x0

    const-string v7, "not_frontal"

    invoke-static/range {v3 .. v10}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;->copy$default(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;FFLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    move-result-object v2

    invoke-virtual {v0, v1, v2}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    const/4 v1, 0x1

    return v1
.end method

.method private final processBlurryDetection(Landroid/graphics/Bitmap;Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings$BlurSettings;Landroid/graphics/RectF;Ljava/lang/Object;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;
    .locals 7
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/graphics/Bitmap;",
            "Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings$BlurSettings;",
            "Landroid/graphics/RectF;",
            "Ljava/lang/Object;",
            "Lkotlin/coroutines/Continuation<",
            "-",
            "Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection;",
            ">;)",
            "Ljava/lang/Object;"
        }
    .end annotation

    instance-of v0, p5, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;

    if-eqz v0, :cond_0

    move-object v0, p5

    check-cast v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;

    iget v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->label:I

    const/high16 v2, -0x80000000

    and-int v3, v1, v2

    if-eqz v3, :cond_0

    sub-int/2addr v1, v2

    iput v1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->label:I

    goto :goto_0

    :cond_0
    new-instance v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;

    invoke-direct {v0, p0, p5}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;-><init>(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;Lkotlin/coroutines/Continuation;)V

    :goto_0
    iget-object p5, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->result:Ljava/lang/Object;

    invoke-static {}, Lkotlin/coroutines/intrinsics/IntrinsicsKt;->getCOROUTINE_SUSPENDED()Ljava/lang/Object;

    move-result-object v1

    iget v2, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->label:I

    const/4 v3, 0x1

    if-eqz v2, :cond_2

    if-ne v2, v3, :cond_1

    iget-object p4, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$4:Ljava/lang/Object;

    iget-object p1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$3:Ljava/lang/Object;

    move-object p3, p1

    check-cast p3, Landroid/graphics/RectF;

    iget-object p1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$2:Ljava/lang/Object;

    move-object p2, p1

    check-cast p2, Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings$BlurSettings;

    iget-object p1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$1:Ljava/lang/Object;

    check-cast p1, Landroid/graphics/Bitmap;

    iget-object v0, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$0:Ljava/lang/Object;

    check-cast v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;

    invoke-static {p5}, Lkotlin/ResultKt;->throwOnFailure(Ljava/lang/Object;)V

    goto :goto_2

    :cond_1
    new-instance p1, Ljava/lang/IllegalStateException;

    const-string p2, "call to \'resume\' before \'invoke\' with coroutine"

    invoke-direct {p1, p2}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V

    throw p1

    :cond_2
    invoke-static {p5}, Lkotlin/ResultKt;->throwOnFailure(Ljava/lang/Object;)V

    if-eqz p2, :cond_3

    invoke-virtual {p2}, Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings$BlurSettings;->isEnable()Z

    move-result p5

    if-ne p5, v3, :cond_3

    move p5, v3

    goto :goto_1

    :cond_3
    const/4 p5, 0x0

    :goto_1
    if-nez p5, :cond_4

    new-instance p2, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Success;

    new-instance p4, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;

    const/4 v3, 0x0

    const/4 v4, 0x0

    const/16 v5, 0xc

    const/4 v6, 0x0

    move-object v0, p4

    move-object v1, p1

    move-object v2, p3

    invoke-direct/range {v0 .. v6}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;-><init>(Landroid/graphics/Bitmap;Landroid/graphics/RectF;FLjava/lang/Object;ILkotlin/jvm/internal/DefaultConstructorMarker;)V

    invoke-direct {p2, p4}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Success;-><init>(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;)V

    return-object p2

    :cond_4
    iget-object p5, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->calculateBlurScore:Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/c;

    invoke-virtual {p5, p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/c;->a(Landroid/graphics/Bitmap;)Lkotlinx/coroutines/flow/Flow;

    move-result-object p5

    invoke-static {}, Lkotlinx/coroutines/Dispatchers;->getIO()Lkotlinx/coroutines/CoroutineDispatcher;

    move-result-object v2

    invoke-static {p5, v2}, Lkotlinx/coroutines/flow/FlowKt;->flowOn(Lkotlinx/coroutines/flow/Flow;Lkotlin/coroutines/CoroutineContext;)Lkotlinx/coroutines/flow/Flow;

    move-result-object p5

    iput-object p0, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$0:Ljava/lang/Object;

    iput-object p1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$1:Ljava/lang/Object;

    iput-object p2, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$2:Ljava/lang/Object;

    iput-object p3, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$3:Ljava/lang/Object;

    iput-object p4, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->L$4:Ljava/lang/Object;

    iput v3, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$processBlurryDetection$1;->label:I

    invoke-static {p5, v0}, Lkotlinx/coroutines/flow/FlowKt;->first(Lkotlinx/coroutines/flow/Flow;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;

    move-result-object p5

    if-ne p5, v1, :cond_5

    return-object v1

    :cond_5
    move-object v0, p0

    :goto_2
    check-cast p5, Lkotlin/Result;

    invoke-virtual {p5}, Lkotlin/Result;->unbox-impl()Ljava/lang/Object;

    move-result-object p5

    invoke-static {p5}, Lkotlin/Result;->isFailure-impl(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_6

    const/4 p5, 0x0

    :cond_6
    check-cast p5, Ljava/lang/Float;

    if-eqz p5, :cond_b

    invoke-virtual {p5}, Ljava/lang/Float;->floatValue()F

    move-result p5

    invoke-virtual {p2}, Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings$BlurSettings;->getThreshold()F

    move-result v1

    cmpg-float v1, p5, v1

    if-gez v1, :cond_7

    new-instance p1, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Failure;

    invoke-direct {p1, p5}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Failure;-><init>(F)V

    return-object p1

    :cond_7
    new-instance v1, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;

    invoke-direct {v1, p1, p3, p5, p4}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;-><init>(Landroid/graphics/Bitmap;Landroid/graphics/RectF;FLjava/lang/Object;)V

    iget-object p1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->blurImages:Ljava/util/List;

    invoke-interface {p1, v1}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J

    move-result-wide p3

    iget-wide v2, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->blurStartTime:J

    const-wide/16 v4, 0x0

    cmp-long p1, v2, v4

    if-nez p1, :cond_8

    iput-wide p3, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->blurStartTime:J

    :cond_8
    iget-wide v2, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->blurStartTime:J

    sub-long/2addr p3, v2

    invoke-virtual {p2}, Lcom/trustingsocial/apisdk/data/settings/flash/FlashLivenessSettings$BlurSettings;->getDuration()I

    move-result p1

    int-to-long p1, p1

    cmp-long p1, p3, p1

    if-ltz p1, :cond_a

    iget-object p1, v0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->blurImages:Ljava/util/List;

    invoke-static {p1}, Lkotlin/collections/CollectionsKt;->maxOrNull(Ljava/lang/Iterable;)Ljava/lang/Comparable;

    move-result-object p1

    check-cast p1, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;

    if-nez p1, :cond_9

    goto :goto_3

    :cond_9
    move-object v1, p1

    :goto_3
    new-instance p1, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Success;

    invoke-direct {p1, v1}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Success;-><init>(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurImage;)V

    return-object p1

    :cond_a
    new-instance p1, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Waiting;

    invoke-direct {p1, p5}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Waiting;-><init>(F)V

    return-object p1

    :cond_b
    new-instance p1, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Failure;

    const/high16 p2, -0x40800000    # -1.0f

    invoke-direct {p1, p2}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel$Companion$BlurryDetection$Failure;-><init>(F)V

    return-object p1
.end method

.method private final process(Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p;Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FaceDetectionConfig;)V
    .locals 11

    instance-of p2, p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$a;

    const-string v0, "/"

    const/4 v1, 0x0

    if-eqz p2, :cond_3

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugInfo:Lkotlinx/coroutines/flow/StateFlow;

    invoke-interface {p2}, Lkotlinx/coroutines/flow/StateFlow;->getValue()Ljava/lang/Object;

    move-result-object v2

    move-object v3, v2

    check-cast v3, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    check-cast p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$a;

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$a;->b()I

    move-result v2

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$a;->c()I

    move-result v4

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "delivered batch "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    const/4 v4, 0x0

    const/4 v5, 0x0

    const/4 v6, 0x0

    const/4 v7, 0x0

    const/16 v9, 0xf

    const/4 v10, 0x0

    invoke-static/range {v3 .. v10}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;->copy$default(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;FFLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    move-result-object v0

    invoke-virtual {p0, p2, v0}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->appState:Lcom/trustingsocial/tvcoresdk/internal/TVAppState;

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/internal/TVAppState;->getSession()Lcom/trustingsocial/tvcoresdk/external/DetectionSession;

    move-result-object p2

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->getMapVideoIds()Ljava/util/Map;

    move-result-object v0

    if-nez v0, :cond_0

    new-instance v0, Ljava/util/LinkedHashMap;

    invoke-direct {v0}, Ljava/util/LinkedHashMap;-><init>()V

    invoke-virtual {p2, v0}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->setMapVideoIds(Ljava/util/Map;)V

    :cond_0
    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->getMapVideoIds()Ljava/util/Map;

    move-result-object p2

    if-eqz p2, :cond_2

    sget-object v0, Lcom/trustingsocial/tvcoresdk/external/BaseDetectionFragment$FrameTag;->SELFIE:Lcom/trustingsocial/tvcoresdk/external/BaseDetectionFragment$FrameTag;

    invoke-interface {p2, v0}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    if-nez v1, :cond_1

    new-instance v1, Ljava/util/LinkedHashSet;

    invoke-direct {v1}, Ljava/util/LinkedHashSet;-><init>()V

    invoke-interface {p2, v0, v1}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    :cond_1
    check-cast v1, Ljava/util/LinkedHashSet;

    :cond_2
    if-eqz v1, :cond_a

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$a;->a()Lcom/trustingsocial/tvcoresdk/external/FrameBatch;

    move-result-object p1

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/external/FrameBatch;->getId()Ljava/lang/String;

    move-result-object p1

    invoke-virtual {v1, p1}, Ljava/util/AbstractCollection;->add(Ljava/lang/Object;)Z

    goto/16 :goto_0

    :cond_3
    instance-of p2, p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$e;

    if-eqz p2, :cond_5

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->waitingForVerifying:Lkotlinx/coroutines/flow/StateFlow;

    sget-object v0, Ljava/lang/Boolean;->FALSE:Ljava/lang/Boolean;

    invoke-virtual {p0, p2, v0}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->appState:Lcom/trustingsocial/tvcoresdk/internal/TVAppState;

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/internal/TVAppState;->getSession()Lcom/trustingsocial/tvcoresdk/external/DetectionSession;

    move-result-object p2

    check-cast p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$e;

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$e;->a()Lcom/trustingsocial/tvcoresdk/internal/domain/entity/h;

    move-result-object p1

    if-eqz p1, :cond_4

    new-instance v0, Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;

    invoke-direct {v0}, Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;-><init>()V

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/entity/h;->a()F

    move-result v1

    invoke-virtual {v0, v1}, Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;->setScore(F)Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;

    move-result-object v0

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/entity/h;->b()Z

    move-result p1

    invoke-virtual {v0, p1}, Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;->setLive(Z)Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;

    move-result-object v1

    :cond_4
    invoke-virtual {p2, v1}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->setLivenessBuilder(Lcom/trustingsocial/tvcoresdk/external/TVLivenessResult$Builder;)V

    goto/16 :goto_0

    :cond_5
    instance-of p2, p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$d;

    if-eqz p2, :cond_6

    invoke-virtual {p0}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->getFailureState()Lkotlinx/coroutines/flow/StateFlow;

    move-result-object p2

    new-instance v0, Lcom/trustingsocial/tvcoresdk/internal/domain/entity/b$a;

    invoke-static {}, Lcom/trustingsocial/apisdk/data/TVApiError;->timeoutError()Lcom/trustingsocial/apisdk/data/TVApiError;

    move-result-object v1

    invoke-static {v1}, Lkotlin/collections/CollectionsKt;->listOf(Ljava/lang/Object;)Ljava/util/List;

    move-result-object v1

    check-cast p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$d;

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$d;->a()J

    move-result-wide v2

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$d;->c()I

    move-result v4

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$d;->b()I

    move-result p1

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "TimedOut in "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v2, v3}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    const-string v2, ", images: "

    invoke-virtual {v5, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    const-string v2, ", frames: "

    invoke-virtual {v5, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    invoke-direct {v0, v1, p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/entity/b$a;-><init>(Ljava/util/List;Ljava/lang/String;)V

    invoke-virtual {p0, p2, v0}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    goto/16 :goto_0

    :cond_6
    instance-of p2, p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$b;

    if-eqz p2, :cond_8

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->debugInfo:Lkotlinx/coroutines/flow/StateFlow;

    invoke-interface {p2}, Lkotlinx/coroutines/flow/StateFlow;->getValue()Ljava/lang/Object;

    move-result-object v1

    move-object v2, v1

    check-cast v2, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    check-cast p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$b;

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$b;->a()I

    move-result v1

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$b;->b()I

    move-result v3

    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    const-string v5, "delivered image "

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v4, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v7

    const/4 v3, 0x0

    const/4 v4, 0x0

    const/4 v5, 0x0

    const/4 v6, 0x0

    const/16 v8, 0xf

    const/4 v9, 0x0

    invoke-static/range {v2 .. v9}, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;->copy$default(Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;FFLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/Object;)Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceUiState$DebugInfo;

    move-result-object v0

    invoke-virtual {p0, p2, v0}, Lcom/trustingsocial/tvcoresdk/internal/base/a;->setData(Lkotlinx/coroutines/flow/StateFlow;Ljava/lang/Object;)V

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->appState:Lcom/trustingsocial/tvcoresdk/internal/TVAppState;

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/internal/TVAppState;->getSession()Lcom/trustingsocial/tvcoresdk/external/DetectionSession;

    move-result-object p2

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->getSelfieImages()Ljava/util/List;

    move-result-object p2

    if-nez p2, :cond_7

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->appState:Lcom/trustingsocial/tvcoresdk/internal/TVAppState;

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/internal/TVAppState;->getSession()Lcom/trustingsocial/tvcoresdk/external/DetectionSession;

    move-result-object p2

    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    invoke-virtual {p2, v0}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->setSelfieImages(Ljava/util/List;)V

    :cond_7
    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->appState:Lcom/trustingsocial/tvcoresdk/internal/TVAppState;

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/internal/TVAppState;->getSession()Lcom/trustingsocial/tvcoresdk/external/DetectionSession;

    move-result-object p2

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->getSelfieImages()Ljava/util/List;

    move-result-object p2

    if-eqz p2, :cond_a

    new-instance v6, Lcom/trustingsocial/tvcoresdk/external/SelfieImage;

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$b;->c()Lcom/trustingsocial/tvcoresdk/external/TVImageClass;

    move-result-object v3

    const/4 v1, 0x0

    const/4 v2, 0x0

    const/4 v4, 0x3

    const/4 v5, 0x0

    move-object v0, v6

    invoke-direct/range {v0 .. v5}, Lcom/trustingsocial/tvcoresdk/external/SelfieImage;-><init>(Lcom/trustingsocial/tvcoresdk/external/selfie/FaceDetectionType;Lcom/trustingsocial/tvcoresdk/external/TVImageClass;Lcom/trustingsocial/tvcoresdk/external/TVImageClass;ILkotlin/jvm/internal/DefaultConstructorMarker;)V

    invoke-interface {p2, v6}, Ljava/util/List;->add(Ljava/lang/Object;)Z

    goto :goto_0

    :cond_8
    instance-of p2, p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$c;

    if-eqz p2, :cond_a

    iget-object p2, p0, Lcom/trustingsocial/tvcoresdk/external/selfie/flash/FlashFaceViewModel;->appState:Lcom/trustingsocial/tvcoresdk/internal/TVAppState;

    invoke-virtual {p2}, Lcom/trustingsocial/tvcoresdk/internal/TVAppState;->getSession()Lcom/trustingsocial/tvcoresdk/external/DetectionSession;

    move-result-object p2

    check-cast p1, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$c;

    invoke-virtual {p1}, Lcom/trustingsocial/tvcoresdk/internal/domain/usecase/p$c;->a()Lcom/trustingsocial/tvcoresdk/external/TVSanityResult;

    move-result-object p1

    if-eqz p1, :cond_9

    new-instance v1, Lcom/trustingsocial/tvcoresdk/external/TVSanityResult$Builder;

    invoke-direct {v1}, Lcom/trustingsocial/tvcoresdk/external/TVSanityResult$Builder;-><init>()V

    invoke-virtual {v1, p1}, Lcom/trustingsocial/tvcoresdk/external/TVSanityResult$Builder;->copy(Lcom/trustingsocial/tvcoresdk/external/TVSanityResult;)V

    :cond_9
    invoke-virtual {p2, v1}, Lcom/trustingsocial/tvcoresdk/external/DetectionSession;->setSelfieSanityBuilder(Lcom/trustingsocial/tvcoresdk/external/TVSanityResult$Builder;)V

    :cond_a
    :goto_0
    return-void
.end method