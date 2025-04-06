import React, { useState, useEffect } from "react";
import Tree from "react-d3-tree";

// Define the structure for a Talent node.
interface TalentNode {
  talentId: string;
  talentName: string;
  description: string;
  requiredLevel: number;
  parentTalent: string | null;
  isActive: boolean;
  children: TalentNode[];
}

interface TalentTreeResponse {
  talentTree: TalentNode[];
}

const containerStyles: React.CSSProperties = {
  width: "100%",
  height: "100vh",
  backgroundColor: "#292f36",
  overflow: "auto",
};

const TalentTreePage: React.FC = () => {
  const [treeData, setTreeData] = useState<TalentNode[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const userId = "user1"; // Replace with dynamic user id as needed

  useEffect(() => {
    const fetchTalentTree = async () => {
      try {
        const response = await fetch("http://localhost:4040/get_talent_tree", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId }),
        });
        const data: TalentTreeResponse = await response.json();
        setTreeData(data.talentTree);
      } catch (error) {
        console.error("Error fetching talent tree:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTalentTree();
  }, [userId]);

  // Transform the talent tree data to the structure expected by react-d3-tree.
  const transformTreeData = (nodes: TalentNode[]): any[] =>
    nodes.map((node) => {
      const children =
        node.children && node.children.length > 0 ? transformTreeData(node.children) : [];
      return {
        // Include the talentId for use in navigation.
        talentId: node.talentId,
        name: `${node.talentName} ${node.isActive ? "(Unlocked)" : "(Locked)"}`,
        attributes: {
          Description: node.description,
          "Required Level": node.requiredLevel,
        },
        children,
      };
    });

  let treeDataTransformed = transformTreeData(treeData);

  // If there are multiple root nodes, combine them under a dummy root node.
  if (treeDataTransformed.length > 1) {
    treeDataTransformed = [
      {
        name: "Talent Tree",
        attributes: {},
        children: treeDataTransformed,
      },
    ];
  }

  if (loading) {
    return <div style={{ textAlign: "center", paddingTop: "50px" }}>Loading talent tree...</div>;
  }

  // Custom node renderer function.
  const renderCustomNodeElement = ({
    nodeDatum,
    toggleNode,
  }: {
    nodeDatum: any;
    toggleNode: () => void;
  }) => (
    <g>
      <circle r={10} fill="#49a078" onClick={toggleNode} />
      <text fill="#9cc5a1" fontSize="14px" x={20} dy={5}>
        {nodeDatum.name}
      </text>
      {nodeDatum.attributes &&
        Object.entries(nodeDatum.attributes).map(([key, value], index) => (
          <text
            key={index}
            fill="#9cc5a1"
            fontSize="12px"
            x={20}
            dy={18 * (index + 2)}
          >
            {`${key}: ${value}`}
          </text>
        ))}
      {/* Button to navigate to the talent page */}
      {nodeDatum.talentId && (
        <foreignObject x={20} y={70} width={100} height={40}>
          <div>
            <button
              style={{
                cursor: "pointer",
                padding: "5px 10px",
                fontSize: "12px",
                backgroundColor: "#49a078",
                border: "none",
                color: "#fff",
              }}
              onClick={(e) => {
                // Prevent propagation to avoid toggling the node when clicking the button
                e.stopPropagation();
                window.location.href = `/talent/${nodeDatum.talentId}`;
              }}
            >
              View Talent
            </button>
          </div>
        </foreignObject>
      )}
    </g>
  );

  return (
    <div style={containerStyles}>
      {/* Inline style block for link styling */}
      <style>{`
        .react-d3-tree .linkPath {
          stroke: #9cc5a1;
          stroke-width: 2px;
        }
      `}</style>
      <h2 style={{ textAlign: "center", padding: "20px 0" }}>Talent Tree</h2>
      <div id="treeWrapper" style={{ width: "1500px", height: "80vh", margin: "0 auto" }}>
        <Tree
          data={treeDataTransformed[0]}
          orientation="vertical"
          translate={{ x: 750, y: 50 }}
          pathFunc="straight"
          collapsible={false}
          separation={{ siblings: 4, nonSiblings: 4 }}
          renderCustomNodeElement={renderCustomNodeElement}
        />
      </div>
    </div>
  );
};

export default TalentTreePage;
