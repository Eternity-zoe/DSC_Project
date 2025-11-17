if (isAVL) {
  recalculateBalanceFactor();

  while (vertexCheckBf != null) {
    var vertexCheckBfClass = iBST[vertexCheckBf]["vertexClassNumber"];

    var bf = iBST[vertexCheckBf]["balanceFactor"];

    cs = createState(iBST);
    cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
    cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
    cs["status"] =
      "Balance factor of {vertexCheckBf} is {bf}.<br>It is {status}."
        .replace("{vertexCheckBf}", vertexCheckBf)
        .replace("{bf}", bf)
        .replace("{status}", Math.abs(bf) <= 1 ? "ok" : "not ok"); // 'Balance factor of {vertexCheckBf} is {bf}.<br>It is {status}.'
    cs["lineNo"] = 2;
    sl.push(cs);

    if (bf == 2) {
      var vertexCheckBfLeft = iBST[vertexCheckBf]["leftChild"];
      var vertexCheckBfLeftClass = iBST[vertexCheckBfLeft]["vertexClassNumber"];
      var bfLeft = iBST[vertexCheckBfLeft]["balanceFactor"];

      cs = createState(iBST);
      cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
      cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
      cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
      cs["vl"][vertexCheckBfLeftClass]["extratext"] = "bf = " + bfLeft;
      cs["status"] = "And balance factor of {vertexCheckBf} is {bf}."
        .replace("{vertexCheckBf}", vertexCheckBfLeft)
        .replace("{bf}", bfLeft); // 'And balance factor of {vertexCheckBf} is {bf}.'
      cs["lineNo"] = 2;
      sl.push(cs);

      if (bfLeft == 1 || bfLeft == 0) {
        rotateRight(vertexCheckBf);

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfLeft)
          cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Rotate right {vertexCheckBF}.".replace(
          "{vertexCheckBf}",
          vertexCheckBf
        ); // 'Rotate right {vertexCheckBf}.'
        cs["lineNo"] = 3;
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfLeft)
          cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Relayout the BST and recompute its height."; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = 3;
        sl.push(cs);
      } else if (bfLeft == -1) {
        var vertexCheckBfLeftRight = iBST[vertexCheckBfLeft]["rightChild"];
        var vertexCheckBfLeftRightClass =
          iBST[vertexCheckBfLeftRight]["vertexClassNumber"];

        rotateLeft(vertexCheckBfLeft);

        cs = createState(iBST);
        cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Rotate left {vertexCheckBf}.".replace(
          "{vertexCheckBf}",
          vertexCheckBf
        ); // 'Rotate left {vertexCheckBf}.'
        cs["lineNo"] = 4;
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST);
        cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Relayout the BST and recompute its height."; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = 4;
        sl.push(cs);

        rotateRight(vertexCheckBf);

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfLeftRight)
          cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Rotate right {vertexCheckBF}.".replace(
          "{vertexCheckBf}",
          vertexCheckBf
        ); // 'Rotate right {vertexCheckBf}.'
        cs["lineNo"] = 4;
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfLeftRight)
          cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Relayout the BST and recompute its height."; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = 4;
        sl.push(cs);
      }
    } else if (bf == -2) {
      var vertexCheckBfRight = iBST[vertexCheckBf]["rightChild"];
      var vertexCheckBfRightClass =
        iBST[vertexCheckBfRight]["vertexClassNumber"];
      var bfRight = iBST[vertexCheckBfRight]["balanceFactor"];

      cs = createState(iBST);
      cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
      cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
      cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
      cs["vl"][vertexCheckBfRightClass]["extratext"] = "bf = " + bfRight;
      cs["status"] = "And balance factor of {vertexCheckBf} is {bf}."
        .replace("{vertexCheckBf}", vertexCheckBfRight)
        .replace("{bf}", bfRight); // 'And balance factor of {vertexCheckBf} is {bf}.'
      cs["lineNo"] = 2;
      sl.push(cs);

      if (bfRight == 1) {
        var vertexCheckBfRightLeft = iBST[vertexCheckBfRight]["leftChild"];
        var vertexCheckBfRightLeftClass =
          iBST[vertexCheckBfRightLeft]["vertexClassNumber"];

        rotateRight(vertexCheckBfRight);

        cs = createState(iBST);
        cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Rotate right {vertexCheckBF}.".replace(
          "{vertexCheckBf}",
          vertexCheckBf
        ); // 'Rotate right {vertexCheckBf}.'
        cs["lineNo"] = 6;
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST);
        cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Relayout the BST and recompute its height."; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = 6;
        sl.push(cs);

        rotateLeft(vertexCheckBf);

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfRightLeft)
          cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Rotate left {vertexCheckBf}.".replace(
          "{vertexCheckBf}",
          vertexCheckBf
        ); // 'Rotate left {vertexCheckBf}.'
        cs["lineNo"] = 6;
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfRightLeft)
          cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Relayout the BST and recompute its height."; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = 6;
        sl.push(cs);
      } else if (bfRight == -1 || bfRight == 0) {
        rotateLeft(vertexCheckBf);

        cs = createState(iBST);
        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfRight)
          cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Rotate left {vertexCheckBf}.".replace(
          "{vertexCheckBf}",
          vertexCheckBf
        ); // 'Rotate left {vertexCheckBf}.'
        cs["lineNo"] = 5;
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST);

        cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
        if (iBST["root"] != vertexCheckBfRight)
          cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = "Relayout the BST and recompute its height."; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = 5;
        sl.push(cs);
      }
    }

    if (vertexCheckBf != iBST["root"]) {
      cs = createState(iBST);
      cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
      //cs["status"] = "Check the parent vertex...";  //status_remove_17
      cs["status"] = "Check the parent vertex...";
      cs["lineNo"] = 2;
      sl.push(cs);
    }

    vertexCheckBf = iBST[vertexCheckBf]["parent"];
  }

  cs = createState(iBST);
  cs["status"] = "The tree is balanced.";
  cs["lineNo"] = 7;
  sl.push(cs);
}
