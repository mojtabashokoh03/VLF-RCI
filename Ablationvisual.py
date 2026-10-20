"""
================================================================
COMPREHENSIVE FEATURE COMPARISON FOR PHISHING DETECTION
===============================================================

This script provides comprehensive evaluation of different feature sets
using multiple tree-based algorithms:
- Random Forest
- Decision Tree
- Gradient Boosting
- XGBoost
- LightGBM
- Extra Trees
- AdaBoost

Evaluation methods:
- 5-Fold Stratified Cross-Validation
- Multiple metrics: Accuracy, Precision, Recall, F1, AUC-ROC
- Statistical analysis and visualization
- Feature importance analysis
- Confusion matrices
===============================================================
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# Machine Learning Libraries
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier,
    AdaBoostClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

# Try to import XGBoost and LightGBM
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False
    print("XGBoost not available. Install: pip install xgboost")

try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False
    print("LightGBM not available. Install: pip install lightgbm")

import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

CSV_FILE = "dataset.csv"
RANDOM_SEED = 42
N_FOLDS = 5
OUTPUT_DIR = "experiment_results"
MAX_FEATURES = 44  # ?????? ????? ????????? ????

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# FEATURE GROUP DEFINITIONS
# ============================================================

def get_feature_groups():
    """Define all feature groups with their column name patterns."""
    
    feature_groups = {
        'Baseline_HOG': {
            'pattern': 'hog_',
            'suffixes': ['_1', '_2'],
            'description': 'Histogram of Oriented Gradients'
        },
        'Baseline_LBP': {
            'pattern': 'lbp_',
            'suffixes': ['_1', '_2'],
            'description': 'Local Binary Patterns'
        },
        'Baseline_SIFT': {
            'pattern': 'sift_',
            'suffixes': ['_1', '_2'],
            'description': 'Scale-Invariant Feature Transform'
        },
        'Baseline_Color': {
            'pattern': ['color_', 'hue_', 'saturation_', 'value_', 'bright_', 'dark_', 'rgb_hist_', 'grid_'],
            'suffixes': ['_1', '_2'],
            'description': 'Color + Spatial Color Features'
        },
        'Baseline_Structural': {
            'pattern': ['edge_', 'horizontal_', 'vertical_', 'layout_', 'struct_grid_', 'whitespace_', 'horizontal_symmetry'],
            'suffixes': ['_1', '_2'],
            'description': 'Structural + Layout Features'
        },
        'Baseline_OCR': {
            'pattern': ['ocr_', 'layout_'],
            'suffixes': ['_1', '_2'],
            'description': 'OCR + Layout Features'
        },
        'Baseline_ResNet50': {
            'pattern': 'resnet50_',
            'suffixes': ['_1', '_2'],
            'description': 'ResNet50 Deep Features'
        },
        'Proposed_RCI': {
            'pattern': ['RCI'],
            'suffixes': ['_1', '_2'],
            'description': 'RCI Features'
        },
        'Proposed_VLF': {
            'pattern': ['VLF_'],
            'suffixes': ['_1', '_2'],
            'description': 'VLF Features'
        },
        'Proposed_VLF_RCI': {
            'pattern': ['VLF_', 'RCI'],
            'suffixes': ['_1', '_2'],
            'description': 'VLF + RCI (Proposed)'
        },
        'Proposed_SVD50_VLF_RCI': {
            'pattern': ['svd50R_1', 'svd50G_1', 'svd50B_1', 'svd50R_2', 'svd50G_2', 'svd50B_2', 'VLF_', 'RCI'],
            'suffixes': ['', '_1', '_2'],
            'svd_features': ['svd50R_1', 'svd50G_1', 'svd50B_1', 'svd50R_2', 'svd50G_2', 'svd50B_2'],
            'description': 'SVD50 + VLF + RCI'
        },
        'Proposed_SVD100_VLF_RCI': {
            'pattern': ['svd100R_1', 'svd100G_1', 'svd100B_1', 'svd100R_2', 'svd100G_2', 'svd100B_2', 'VLF_', 'RCI'],
            'suffixes': ['', '_1', '_2'],
            'svd_features': ['svd100R_1', 'svd100G_1', 'svd100B_1', 'svd100R_2', 'svd100G_2', 'svd100B_2'],
            'description': 'SVD100 + VLF + RCI'
        },
        'Proposed_SVD150_VLF_RCI': {
            'pattern': ['svd150R_1', 'svd150G_1', 'svd150B_1', 'svd150R_2', 'svd150G_2', 'svd150B_2', 'VLF_', 'RCI'],
            'suffixes': ['', '_1', '_2'],
            'svd_features': ['svd150R_1', 'svd150G_1', 'svd150B_1', 'svd150R_2', 'svd150G_2', 'svd150B_2'],
            'description': 'SVD150 + VLF + RCI'
        },
        'Proposed_SVD200_VLF_RCI': {
            'pattern': ['svd200R_1', 'svd200G_1', 'svd200B_1', 'svd200R_2', 'svd200G_2', 'svd200B_2', 'VLF_', 'RCI'],
            'suffixes': ['', '_1', '_2'],
            'svd_features': ['svd200R_1', 'svd200G_1', 'svd200B_1', 'svd200R_2', 'svd200G_2', 'svd200B_2'],
            'description': 'SVD200 + VLF + RCI'
        },
        'Proposed_SVD100': {
            'pattern': ['svd100R_1', 'svd100G_1', 'svd100B_1', 'svd100R_2', 'svd100G_2', 'svd100B_2'],
            'suffixes': ['', '_1', '_2'],
            'svd_features': ['svd100R_1', 'svd100G_1', 'svd100B_1', 'svd100R_2', 'svd100G_2', 'svd100B_2'],
            'description': 'SVD100 Features'
        }
    }
    
    return feature_groups


def select_features_by_pattern(df, patterns, suffixes, svd_features=None):
    """
    Select columns from DataFrame based on patterns.
    """
    all_columns = df.columns.tolist()
    selected = []
    
    if isinstance(patterns, str):
        patterns = [patterns]
    
    # Special handling for SVD features
    if svd_features:
        for svd_feat in svd_features:
            if svd_feat in all_columns:
                selected.append(svd_feat)
    
    for col in all_columns:
        if col in ['idphish', 'url', 'isphish']:
            continue
        
        if svd_features and col in svd_features:
            continue
            
        has_suffix = any(col.endswith(suffix) for suffix in suffixes) if suffixes else True
        
        matches_pattern = any(pattern in col for pattern in patterns) if patterns != ['all'] else True
        if matches_pattern and has_suffix:
            selected.append(col)
    
    return selected


def get_features_for_group(df, group_name, group_config):
    """Get feature columns for a specific group."""
    patterns = group_config['pattern']
    suffixes = group_config.get('suffixes', ['_1', '_2'])
    svd_features = group_config.get('svd_features', None)
    
    if patterns == 'all':
        all_cols = df.columns.tolist()
        features = [col for col in all_cols if col not in ['idphish', 'url', 'isphish']]
        return features
    
    return select_features_by_pattern(df, patterns, suffixes, svd_features=svd_features)


# ============================================================
# DATA CLEANING AND PREPARATION
# ============================================================

def clean_data(X):
    """Clean data by handling NaN, infinity, and extreme values."""
    X = np.where(np.isinf(X), np.nan, X)
    
    for i in range(X.shape[1]):
        col = X[:, i]
        if not np.all(np.isnan(col)):
            mean_val = np.nanmean(col)
            std_val = np.nanstd(col)
            if std_val > 0:
                threshold = 3 * std_val
                X[np.abs(col - mean_val) > threshold, i] = np.nan
    
    return X


def prepare_data(df, feature_columns):
    """Prepare X and y data for training with robust error handling."""
    if 'isphish' not in df.columns:
        print("WARNING: 'isphish' column not found!")
        return None, None, None
    
    if not feature_columns:
        print("WARNING: No feature columns provided!")
        return None, None, None
    
    try:
        X_df = df[feature_columns].copy()
    except KeyError as e:
        print(f"WARNING: Some features not found: {e}")
        existing_cols = [col for col in feature_columns if col in df.columns]
        if not existing_cols:
            print("ERROR: No valid feature columns found!")
            return None, None, None
        X_df = df[existing_cols].copy()
        feature_columns = existing_cols
    
    if X_df.empty:
        print("ERROR: Feature data is empty!")
        return None, None, None
    
    X = np.asarray(X_df, dtype=np.float64)
    X = clean_data(X)
    
    all_nan_cols = np.all(np.isnan(X), axis=0)
    if np.any(all_nan_cols):
        print(f"WARNING: Removing {np.sum(all_nan_cols)} columns with all NaN values")
        X = X[:, ~all_nan_cols]
        feature_columns = [col for i, col in enumerate(feature_columns) if not all_nan_cols[i]]
    
    if X.shape[1] == 0:
        print("ERROR: No valid features remaining after cleaning!")
        return None, None, None
    
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    
    if np.any(np.isnan(X_imputed)) or np.any(np.isinf(X_imputed)):
        X_imputed = np.nan_to_num(X_imputed, nan=0.0, posinf=0.0, neginf=0.0)
    
    X_imputed = X_imputed.astype(np.float32)
    
    scaler = StandardScaler()
    try:
        X_scaled = scaler.fit_transform(X_imputed)
    except ValueError as e:
        print(f"WARNING: Scaling failed: {e}")
        X_scaled = X_imputed
    
    y = np.asarray(df['isphish'].values, dtype=np.int32)
    
    valid_idx = ~np.isnan(y)
    if not np.all(valid_idx):
        print(f"WARNING: Removing {np.sum(~valid_idx)} rows with NaN labels")
        X_scaled = X_scaled[valid_idx]
        y = y[valid_idx]
    
    if np.any(np.isnan(X_scaled)) or np.any(np.isinf(X_scaled)):
        X_scaled = np.nan_to_num(X_scaled, nan=0.0, posinf=0.0, neginf=0.0)
    
    return X_scaled, y, feature_columns


# ============================================================
# FEATURE SELECTION FUNCTION
# ============================================================

def select_top_features(X, y, n_features=44, method='mutual_info'):
    """
    Select top n_features using specified method.
    """
    if X.shape[1] <= n_features:
        return X, list(range(X.shape[1]))
    
    try:
        if method == 'mutual_info':
            selector = SelectKBest(mutual_info_classif, k=n_features)
        else:  # default to f_classif
            selector = SelectKBest(f_classif, k=n_features)
        
        X_selected = selector.fit_transform(X, y)
        selected_indices = selector.get_support(indices=True)
        
        return X_selected, selected_indices
    except Exception as e:
        print(f"  WARNING: Feature selection failed: {e}. Using first {n_features} features.")
        return X[:, :n_features], list(range(n_features))


# ============================================================
# ALGORITHM DEFINITIONS
# ============================================================

def get_algorithms():
    """Define all algorithms to evaluate."""
    
    algorithms = {
        'Random Forest': {
            'classifier': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=RANDOM_SEED,
                n_jobs=-1
            ),
            'description': 'Random Forest Classifier'
        },
        'Decision Tree': {
            'classifier': DecisionTreeClassifier(
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=RANDOM_SEED
            ),
            'description': 'Decision Tree Classifier'
        },
        'Gradient Boosting': {
            'classifier': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=RANDOM_SEED
            ),
            'description': 'Gradient Boosting Classifier'
        },
        'Extra Trees': {
            'classifier': ExtraTreesClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=RANDOM_SEED,
                n_jobs=-1
            ),
            'description': 'Extra Trees Classifier'
        },
        'AdaBoost': {
            'classifier': AdaBoostClassifier(
                n_estimators=100,
                learning_rate=0.1,
                random_state=RANDOM_SEED
            ),
            'description': 'AdaBoost Classifier'
        }
    }
    
    if XGB_AVAILABLE:
        algorithms['XGBoost'] = {
            'classifier': xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=RANDOM_SEED,
                use_label_encoder=False,
                eval_metric='logloss'
            ),
            'description': 'XGBoost Classifier'
        }
    
    if LGB_AVAILABLE:
        algorithms['LightGBM'] = {
            'classifier': lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                num_leaves=31,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=RANDOM_SEED,
                verbose=-1
            ),
            'description': 'LightGBM Classifier'
        }
    
    return algorithms


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate_features(X, y, feature_name, algorithm_name, classifier, n_folds=5):
    """
    Evaluate features using Stratified K-Fold Cross Validation.
    """
    
    if X is None or y is None:
        return None
    
    if len(X) == 0 or len(y) == 0:
        return None
    
    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        return None
    
    # Determine number of folds
    n_splits = min(n_folds, np.min(np.bincount(y)))
    if n_splits < 2:
        n_splits = 2
    
    try:
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_SEED)
    except ValueError:
        from sklearn.model_selection import KFold
        skf = KFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_SEED)
    
    # Initialize lists
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    auc_scores = []
    
    all_y_true = []
    all_y_pred = []
    all_y_prob = []
    
    fold = 1
    for train_index, test_index in skf.split(X, y):
        try:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            
            # Check if training data has both classes
            if len(np.unique(y_train)) < 2:
                continue
            
            classifier.fit(X_train, y_train)
            
            y_pred = classifier.predict(X_test)
            try:
                y_prob = classifier.predict_proba(X_test)[:, 1]
            except:
                y_prob = np.zeros_like(y_pred)
            
            all_y_true.extend(y_test)
            all_y_pred.extend(y_pred)
            all_y_prob.extend(y_prob)
            
            accuracies.append(accuracy_score(y_test, y_pred))
            precisions.append(precision_score(y_test, y_pred, average='binary', zero_division=0))
            recalls.append(recall_score(y_test, y_pred, average='binary', zero_division=0))
            f1_scores.append(f1_score(y_test, y_pred, average='binary', zero_division=0))
            
            try:
                auc_scores.append(roc_auc_score(y_test, y_prob))
            except:
                auc_scores.append(0.5)
            
            fold += 1
            
        except Exception as e:
            print(f"  WARNING: Fold {fold} failed: {e}")
            continue
    
    if not accuracies:
        return None
    
    # Overall metrics
    overall_accuracy = accuracy_score(all_y_true, all_y_pred)
    overall_precision = precision_score(all_y_true, all_y_pred, average='binary', zero_division=0)
    overall_recall = recall_score(all_y_true, all_y_pred, average='binary', zero_division=0)
    overall_f1 = f1_score(all_y_true, all_y_pred, average='binary', zero_division=0)
    try:
        overall_auc = roc_auc_score(all_y_true, all_y_prob)
    except:
        overall_auc = 0.5
    
    cm = confusion_matrix(all_y_true, all_y_pred)
    if cm.size == 4:
        tn, fp, fn, tp = cm.ravel()
    else:
        tn, fp, fn, tp = 0, 0, 0, 0
    
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    metrics = {
        'feature_group': feature_name,
        'algorithm': algorithm_name,
        'n_features': X.shape[1],
        'n_samples': X.shape[0],
        'n_folds': len(accuracies),
        'accuracy': overall_accuracy,
        'precision': overall_precision,
        'recall': overall_recall,
        'f1_score': overall_f1,
        'auc_roc': overall_auc,
        'specificity': specificity,
        'sensitivity': sensitivity,
        'accuracy_mean': np.mean(accuracies) if accuracies else 0,
        'accuracy_std': np.std(accuracies) if accuracies else 0,
        'precision_mean': np.mean(precisions) if precisions else 0,
        'precision_std': np.std(precisions) if precisions else 0,
        'recall_mean': np.mean(recalls) if recalls else 0,
        'recall_std': np.std(recalls) if recalls else 0,
        'f1_mean': np.mean(f1_scores) if f1_scores else 0,
        'f1_std': np.std(f1_scores) if f1_scores else 0,
        'auc_mean': np.mean(auc_scores) if auc_scores else 0,
        'auc_std': np.std(auc_scores) if auc_scores else 0,
        'true_positives': tp,
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn
    }
    
    return metrics


# ============================================================
# VISUALIZATION FUNCTIONS
# ============================================================

def create_all_visualizations(results_df, feature_groups, algorithms):
    """
    Create comprehensive visualization plots for the paper.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set style for publication quality
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("husl")
    
    # 1. Performance Comparison across all metrics
    create_performance_comparison(results_df, timestamp)
    
    # 2. Feature Group Comparison (Best Algorithm)
    create_feature_group_comparison(results_df, timestamp)
    
    # 3. Algorithm Comparison (Best Feature Group)
    create_algorithm_comparison(results_df, timestamp)
    
    # 4. Heatmap of performance metrics
    create_performance_heatmap(results_df, timestamp)
    
    # 5. Radar chart for top methods
    create_radar_chart(results_df, timestamp)
    
    # 6. Confusion Matrix Heatmaps for each feature group
    create_confusion_matrices(results_df, timestamp)
    
    # 7. Feature importance (if available)
    create_feature_importance_plots(results_df, timestamp)
    
    # 8. Performance vs Feature Count
    create_performance_vs_features(results_df, timestamp)
    
    # 9. Box plots for cross-validation results
    create_cv_boxplots(results_df, timestamp)
    
    # 10. Paired Comparison Charts
    create_paired_comparison(results_df, timestamp)
    
    print(f"\nAll visualizations saved to: {OUTPUT_DIR}/")


def create_performance_comparison(results_df, timestamp):
    """Create comprehensive performance comparison plot."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Comprehensive Performance Comparison', fontsize=16, fontweight='bold')
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'auc_roc', 'specificity']
    titles = ['Accuracy Comparison', 'Precision Comparison', 'Recall Comparison',
              'F1-Score Comparison', 'AUC-ROC Comparison', 'Specificity Comparison']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx // 3, idx % 3]
        
        # Pivot data for grouped bar chart
        pivot_data = results_df.pivot_table(
            index='feature_group', 
            columns='algorithm', 
            values=metric,
            aggfunc='mean'
        ).fillna(0)
        
        # Plot grouped bar chart
        pivot_data.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('Feature Group', fontsize=10)
        ax.set_ylabel('Score', fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/performance_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_feature_group_comparison(results_df, timestamp):
    """Create feature group comparison using best performing algorithm."""
    # Find best algorithm for each feature group
    best_algo_idx = results_df.groupby('feature_group')['f1_score'].idxmax()
    best_results = results_df.loc[best_algo_idx]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Feature Group Comparison (Best Algorithm)', fontsize=16, fontweight='bold')
    
    # Sort by F1 score
    best_results_sorted = best_results.sort_values('f1_score', ascending=False)
    
    # Plot F1 Score and Accuracy
    x = np.arange(len(best_results_sorted))
    width = 0.35
    
    ax1 = axes[0]
    bars1 = ax1.bar(x - width/2, best_results_sorted['f1_score'], width, label='F1-Score', color='royalblue', alpha=0.8)
    bars2 = ax1.bar(x + width/2, best_results_sorted['accuracy'], width, label='Accuracy', color='coral', alpha=0.8)
    ax1.set_xlabel('Feature Group', fontsize=12)
    ax1.set_ylabel('Score', fontsize=12)
    ax1.set_title('F1-Score vs Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(best_results_sorted['feature_group'], rotation=45, ha='right', fontsize=10)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=7, rotation=0)
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=7, rotation=0)
    
    # Plot AUC-ROC and F1
    ax2 = axes[1]
    bars3 = ax2.bar(x - width/2, best_results_sorted['auc_roc'], width, label='AUC-ROC', color='forestgreen', alpha=0.8)
    bars4 = ax2.bar(x + width/2, best_results_sorted['f1_score'], width, label='F1-Score', color='royalblue', alpha=0.8)
    ax2.set_xlabel('Feature Group', fontsize=12)
    ax2.set_ylabel('Score', fontsize=12)
    ax2.set_title('AUC-ROC vs F1-Score', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(best_results_sorted['feature_group'], rotation=45, ha='right', fontsize=10)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars3:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=7, rotation=0)
    for bar in bars4:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=7, rotation=0)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/feature_group_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_algorithm_comparison(results_df, timestamp):
    """Create algorithm comparison using best performing feature group."""
    # Find best feature group for each algorithm
    best_feat_idx = results_df.groupby('algorithm')['f1_score'].idxmax()
    best_results = results_df.loc[best_feat_idx]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Algorithm Comparison (Best Feature Group)', fontsize=16, fontweight='bold')
    
    # Sort by F1 score
    best_results_sorted = best_results.sort_values('f1_score', ascending=False)
    
    x = np.arange(len(best_results_sorted))
    width = 0.35
    
    ax1 = axes[0]
    bars1 = ax1.bar(x - width/2, best_results_sorted['f1_score'], width, label='F1-Score', color='royalblue', alpha=0.8)
    bars2 = ax1.bar(x + width/2, best_results_sorted['accuracy'], width, label='Accuracy', color='coral', alpha=0.8)
    ax1.set_xlabel('Algorithm', fontsize=12)
    ax1.set_ylabel('Score', fontsize=12)
    ax1.set_title('F1-Score vs Accuracy by Algorithm', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(best_results_sorted['algorithm'], rotation=45, ha='right', fontsize=10)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    ax2 = axes[1]
    bars3 = ax2.bar(x - width/2, best_results_sorted['auc_roc'], width, label='AUC-ROC', color='forestgreen', alpha=0.8)
    bars4 = ax2.bar(x + width/2, best_results_sorted['precision'], width, label='Precision', color='orange', alpha=0.8)
    ax2.set_xlabel('Algorithm', fontsize=12)
    ax2.set_ylabel('Score', fontsize=12)
    ax2.set_title('AUC-ROC vs Precision by Algorithm', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(best_results_sorted['algorithm'], rotation=45, ha='right', fontsize=10)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    
    for bar in bars3:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    for bar in bars4:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/algorithm_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_performance_heatmap(results_df, timestamp):
    """Create heatmap of performance metrics."""
    # Create pivot tables for each metric
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'auc_roc', 'specificity']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Performance Metrics Heatmaps', fontsize=16, fontweight='bold')
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 3, idx % 3]
        
        pivot_data = results_df.pivot_table(
            index='feature_group',
            columns='algorithm',
            values=metric,
            aggfunc='mean'
        ).fillna(0)
        
        # Sort by average performance
        pivot_data = pivot_data.reindex(pivot_data.mean(axis=1).sort_values(ascending=True).index)
        
        im = sns.heatmap(pivot_data, ax=ax, cmap='RdYlGn', annot=True, fmt='.3f',
                         cbar_kws={'label': metric.title()}, cbar=True)
        ax.set_title(f'{metric.title()} Heatmap', fontsize=12, fontweight='bold')
        ax.set_xlabel('Algorithm', fontsize=10)
        ax.set_ylabel('Feature Group', fontsize=10)
        
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/performance_heatmap_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_radar_chart(results_df, timestamp):
    """Create radar chart for top performing combinations."""
    # Get top 5 feature groups based on average F1 score
    top_features = results_df.groupby('feature_group')['f1_score'].mean().sort_values(ascending=False).head(5).index
    top_results = results_df[results_df['feature_group'].isin(top_features)]
    
    # For each feature group, get the best algorithm
    best_results = top_results.loc[top_results.groupby('feature_group')['f1_score'].idxmax()]
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'auc_roc', 'specificity']
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(best_results)))
    
    for idx, (_, row) in enumerate(best_results.iterrows()):
        values = [row[metric] for metric in metrics]
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, label=f"{row['feature_group']} ({row['algorithm']})", 
                color=colors[idx])
        ax.fill(angles, values, alpha=0.15, color=colors[idx])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([m.title() for m in metrics], fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_title('Performance Radar Chart - Top 5 Feature Groups', fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5), fontsize=9)
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/radar_chart_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_confusion_matrices(results_df, timestamp):
    """Create confusion matrix heatmaps for each feature group using best algorithm."""
    # Get best algorithm for each feature group
    best_algo_idx = results_df.groupby('feature_group')['f1_score'].idxmax()
    best_results = results_df.loc[best_algo_idx]
    
    # Select top performing feature groups
    top_features = best_results.sort_values('f1_score', ascending=False).head(8)['feature_group'].tolist()
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Confusion Matrices - Top Performing Feature Groups', fontsize=16, fontweight='bold')
    
    for idx, feature in enumerate(top_features):
        ax = axes[idx // 4, idx % 4]
        row = best_results[best_results['feature_group'] == feature].iloc[0]
        
        cm = np.array([[row['true_negatives'], row['false_positives']],
                       [row['false_negatives'], row['true_positives']]])
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['Predicted 0', 'Predicted 1'],
                    yticklabels=['Actual 0', 'Actual 1'])
        ax.set_title(f"{feature}\nF1={row['f1_score']:.3f}, Acc={row['accuracy']:.3f}", 
                     fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/confusion_matrices_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_feature_importance_plots(results_df, timestamp):
    """Create feature importance plots."""
    # This is a placeholder - actual feature importance would require model training
    # We'll create a simple visualization of feature counts vs performance
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Group by feature group and calculate stats
    stats = results_df.groupby('feature_group').agg({
        'n_features': 'first',
        'f1_score': 'mean',
        'accuracy': 'mean',
        'auc_roc': 'mean'
    }).reset_index()
    
    # Create scatter plot
    scatter = ax.scatter(stats['n_features'], stats['f1_score'], 
                        s=stats['accuracy'] * 500, 
                        c=stats['auc_roc'], 
                        cmap='RdYlGn', 
                        alpha=0.6,
                        edgecolors='black', 
                        linewidth=0.5)
    
    # Add labels for each point
    for idx, row in stats.iterrows():
        ax.annotate(row['feature_group'], 
                   (row['n_features'], row['f1_score']),
                   fontsize=8, alpha=0.7,
                   ha='center', va='bottom')
    
    ax.set_xlabel('Number of Features', fontsize=12)
    ax.set_ylabel('Average F1-Score', fontsize=12)
    ax.set_title('Feature Count vs Performance\n(Size: Accuracy, Color: AUC-ROC)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter)
    cbar.set_label('AUC-ROC', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/feature_importance_plot_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_performance_vs_features(results_df, timestamp):
    """Create performance vs features plot."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Performance vs Number of Features', fontsize=16, fontweight='bold')
    
    # Get best algorithm for each feature group
    best_algo_idx = results_df.groupby('feature_group')['f1_score'].idxmax()
    best_results = results_df.loc[best_algo_idx]
    
    # Sort by feature count
    best_results_sorted = best_results.sort_values('n_features')
    
    ax1 = axes[0]
    ax1.plot(best_results_sorted['n_features'], best_results_sorted['f1_score'], 
             'o-', label='F1-Score', color='royalblue', linewidth=2, markersize=8)
    ax1.plot(best_results_sorted['n_features'], best_results_sorted['accuracy'], 
             's-', label='Accuracy', color='coral', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Features', fontsize=12)
    ax1.set_ylabel('Score', fontsize=12)
    ax1.set_title('F1-Score & Accuracy vs Features', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes[1]
    ax2.plot(best_results_sorted['n_features'], best_results_sorted['auc_roc'], 
             'd-', label='AUC-ROC', color='forestgreen', linewidth=2, markersize=8)
    ax2.plot(best_results_sorted['n_features'], best_results_sorted['precision'], 
             '^-', label='Precision', color='orange', linewidth=2, markersize=8)
    ax2.plot(best_results_sorted['n_features'], best_results_sorted['recall'], 
             'v-', label='Recall', color='purple', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Features', fontsize=12)
    ax2.set_ylabel('Score', fontsize=12)
    ax2.set_title('AUC-ROC, Precision & Recall vs Features', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/performance_vs_features_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_cv_boxplots(results_df, timestamp):
    """Create box plots for cross-validation results."""
    # Get top feature groups
    top_features = results_df.groupby('feature_group')['f1_mean'].mean().sort_values(ascending=False).head(8).index
    top_results = results_df[results_df['feature_group'].isin(top_features)]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Cross-Validation Performance Distribution', fontsize=16, fontweight='bold')
    
    metrics = [
        ('accuracy_mean', 'accuracy_std', 'Accuracy'),
        ('precision_mean', 'precision_std', 'Precision'),
        ('recall_mean', 'recall_std', 'Recall'),
        ('f1_mean', 'f1_std', 'F1-Score'),
        ('auc_mean', 'auc_std', 'AUC-ROC')
    ]
    
    for idx, (mean_col, std_col, title) in enumerate(metrics):
        ax = axes[idx // 3, idx % 3]
        
        # Prepare data for box plot
        data = []
        labels = []
        for feature in top_features:
            feature_data = top_results[top_results['feature_group'] == feature]
            if not feature_data.empty:
                # Use mean as center and std as spread
                means = feature_data[mean_col].values
                stds = feature_data[std_col].values
                data.append(means)
                labels.append(feature[:20])  # Truncate long names
        
        if data:
            ax.boxplot(data, labels=labels, showmeans=True)
            ax.set_title(f'{title} Distribution', fontsize=12, fontweight='bold')
            ax.set_xlabel('Feature Group', fontsize=10)
            ax.set_ylabel(title, fontsize=10)
            ax.tick_params(axis='x', rotation=45, labelsize=8)
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/cv_boxplots_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_paired_comparison(results_df, timestamp):
    """Create paired comparison charts."""
    # Compare proposed method against baselines
    proposed_methods = ['Proposed_VLF_RCI', 'Proposed_SVD50_VLF_RCI', 'Proposed_SVD100_VLF_RCI']
    baseline_methods = ['Baseline_HOG', 'Baseline_LBP', 'Baseline_SIFT', 'Baseline_Color', 
                       'Baseline_Structural', 'Baseline_OCR', 'Baseline_ResNet50']
    
    # Filter results
    proposed_results = results_df[results_df['feature_group'].isin(proposed_methods)]
    baseline_results = results_df[results_df['feature_group'].isin(baseline_methods)]
    
    if proposed_results.empty or baseline_results.empty:
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate improvements
    improvements = []
    for _, proposed in proposed_results.iterrows():
        best_baseline = baseline_results.loc[baseline_results['f1_score'].idxmax()]
        improvement = ((proposed['f1_score'] - best_baseline['f1_score']) / best_baseline['f1_score']) * 100
        improvements.append({
            'method': proposed['feature_group'],
            'algorithm': proposed['algorithm'],
            'f1_score': proposed['f1_score'],
            'improvement': improvement
        })
    
    improvements_df = pd.DataFrame(improvements)
    improvements_df = improvements_df.sort_values('improvement', ascending=False)
    
    # Create bar chart
    bars = ax.bar(improvements_df['method'] + ' (' + improvements_df['algorithm'] + ')', 
                  improvements_df['improvement'],
                  color='green' if all(improvements_df['improvement'] > 0) else 'red')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Method (Algorithm)', fontsize=12)
    ax.set_ylabel('Improvement over Best Baseline (%)', fontsize=12)
    ax.set_title('Proposed Method Improvement over Best Baseline', fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/improvement_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """
    Main function to run comprehensive feature comparison.
    """
    
    print("="*80)
    print("COMPREHENSIVE FEATURE COMPARISON FOR PHISHING DETECTION")
    print("="*80)
    print(f"Experiment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Maximum Features per Group: {MAX_FEATURES}")
    print("="*80)
    
    # Load data
    print(f"\nLoading data from: {CSV_FILE}")
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"Data loaded: {len(df)} samples, {len(df.columns)} columns")
    except Exception as e:
        print(f"ERROR: Could not load data: {e}")
        return
    
    if 'isphish' not in df.columns:
        print("\nERROR: 'isphish' column not found!")
        return
    
    print(f"\nClass distribution:")
    print(f"  Legitimate (0): {sum(df['isphish'] == 0)}")
    print(f"  Phishing (1): {sum(df['isphish'] == 1)}")
    
    # Get feature groups
    feature_groups = get_feature_groups()
    algorithms = get_algorithms()
    
    # Display available algorithms
    print("\n" + "-"*60)
    print("Available Algorithms:")
    print("-"*60)
    for name, config in algorithms.items():
        print(f"  {name}: {config['description']}")
        if name in ['XGBoost', 'LightGBM']:
            print(f"    ({'Available' if True else 'Not Available'})")
    
    # Display feature groups
    print("\n" + "-"*60)
    print("Feature Groups:")
    print("-"*60)
    for name, config in feature_groups.items():
        features = get_features_for_group(df, name, config)
        print(f"  {name:30} : {len(features):5} features - {config['description']}")
    
    # Collect features
    group_features = {}
    for group_name, group_config in feature_groups.items():
        features = get_features_for_group(df, group_name, group_config)
        group_features[group_name] = features
    
    # Run experiments
    all_results = []
    
    print("\n" + "="*80)
    print("RUNNING EXPERIMENTS")
    print("="*80)
    
    for group_name, features in group_features.items():
        if not features:
            print(f"\nSkipping {group_name}: No features found")
            continue
        
        print(f"\n{'-'*60}")
        print(f"Feature Group: {group_name}")
        print(f"  Number of features: {len(features)}")
        
        # Prepare data once for all algorithms
        X, y, feature_names = prepare_data(df, features)
        
        if X is None or y is None:
            print(f"  ERROR: Could not prepare data")
            continue
        
        # ====== ????? ???: ?????? ????? ======
        if X is not None and y is not None and X.shape[1] > MAX_FEATURES:
            print(f"  Selecting top {MAX_FEATURES} features from {X.shape[1]} features...")
            try:
                X_selected, selected_indices = select_top_features(X, y, n_features=MAX_FEATURES, method='mutual_info')
                selected_feature_names = [feature_names[i] for i in selected_indices]
                X = X_selected
                feature_names = selected_feature_names
                print(f"  Selected {len(feature_names)} features")
            except Exception as e:
                print(f"  WARNING: Feature selection failed: {e}. Using all features.")
        # ====== ????? ??? ????? ??? ======
        
        print(f"  Data shape: {X.shape}")
        
        # Evaluate with each algorithm
        for algo_name, algo_config in algorithms.items():
            print(f"  Testing: {algo_name}...", end=" ")
            
            metrics = evaluate_features(
                X, y, 
                group_name, 
                algo_name,
                algo_config['classifier'],
                N_FOLDS
            )
            
            if metrics is None:
                print("FAILED")
                continue
            
            all_results.append(metrics)
            print(f"F1={metrics['f1_score']:.4f}, Acc={metrics['accuracy']:.4f}")
    
    if not all_results:
        print("\nERROR: No results obtained!")
        return
    
    # Create results DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"{OUTPUT_DIR}/experiment_results_{timestamp}.csv"
    results_df.to_csv(results_file, index=False)
    print(f"\nResults saved to: {results_file}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    # Best overall
    best_f1 = results_df.loc[results_df['f1_score'].idxmax()]
    print(f"\nBest Overall (F1-Score):")
    print(f"  Feature Group: {best_f1['feature_group']}")
    print(f"  Algorithm: {best_f1['algorithm']}")
    print(f"  F1-Score: {best_f1['f1_score']:.4f}")
    print(f"  Accuracy: {best_f1['accuracy']:.4f}")
    print(f"  AUC-ROC: {best_f1['auc_roc']:.4f}")
    print(f"  Number of Features: {best_f1['n_features']}")
    
    # Best per algorithm
    print("\n" + "-"*60)
    print("Best Performance per Algorithm:")
    print("-"*60)
    for algo in results_df['algorithm'].unique():
        best = results_df[results_df['algorithm'] == algo].loc[
            results_df[results_df['algorithm'] == algo]['f1_score'].idxmax()
        ]
        print(f"  {algo:20} : F1={best['f1_score']:.4f}, Feature={best['feature_group']}, n_features={best['n_features']}")
    
    # Best per feature group
    print("\n" + "-"*60)
    print("Best Performance per Feature Group:")
    print("-"*60)
    for feat in results_df['feature_group'].unique():
        best = results_df[results_df['feature_group'] == feat].loc[
            results_df[results_df['feature_group'] == feat]['f1_score'].idxmax()
        ]
        print(f"  {feat:30} : F1={best['f1_score']:.4f}, Algo={best['algorithm']}, n_features={best['n_features']}")
    
    # Proposed method comparison
    print("\n" + "-"*60)
    print("Proposed Methods Comparison:")
    print("-"*60)
    
    proposed_methods = [g for g in feature_groups.keys() if 'Proposed' in g]
    for method in proposed_methods:
        method_results = results_df[results_df['feature_group'] == method]
        if not method_results.empty:
            best = method_results.loc[method_results['f1_score'].idxmax()]
            print(f"  {method:30} : F1={best['f1_score']:.4f}, Algo={best['algorithm']}, n_features={best['n_features']}")
    
    # Create comprehensive visualizations
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    create_all_visualizations(results_df, feature_groups, algorithms)
    
    print("\n" + "="*80)
    print("EXPERIMENT COMPLETE!")
    print(f"Results and visualizations saved to: {OUTPUT_DIR}/")
    print("="*80)
    
    return results_df


if __name__ == "__main__":
    try:
        results_df = main()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()