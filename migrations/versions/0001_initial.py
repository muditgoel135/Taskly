"""initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(32), nullable=False, server_default='student'),
        sa.Column('created_at', sa.DateTime)
    )
    op.create_table('pages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(255)),
        sa.Column('content', sa.Text),
        sa.Column('pinned', sa.Boolean, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime)
    )
    op.create_table('databases',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(255)),
        sa.Column('schema', sa.JSON)
    )
    op.create_table('database_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('database_id', sa.Integer, sa.ForeignKey('databases.id')),
        sa.Column('data', sa.JSON)
    )
    op.create_table('tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('due_at', sa.DateTime),
        sa.Column('priority', sa.Integer, server_default='1'),
        sa.Column('done', sa.Boolean, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime)
    )
    op.create_table('task_subtasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id')),
        sa.Column('title', sa.String(255)),
        sa.Column('done', sa.Boolean, server_default=sa.false())
    )
    op.create_table('events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('start_at', sa.DateTime),
        sa.Column('end_at', sa.DateTime),
        sa.Column('location', sa.String(255))
    )
    op.create_table('habits',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(255)),
        sa.Column('streak', sa.Integer, server_default='0'),
        sa.Column('active', sa.Boolean, server_default=sa.true())
    )
    op.create_table('goals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(255)),
        sa.Column('progress', sa.Integer, server_default='0')
    )
    op.create_table('focus_sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id')),
        sa.Column('minutes', sa.Integer, server_default='25')
    )
    op.create_table('sounds',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('url', sa.String(512))
    )
    op.create_table('integrations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('kind', sa.String(64)),
        sa.Column('access_token', sa.String(1024))
    )
    op.create_table('notifications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('channel', sa.String(32)),
        sa.Column('payload', sa.String(1024)),
        sa.Column('sent', sa.Boolean, server_default=sa.false())
    )
    op.create_table('memberships',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('page_id', sa.Integer, sa.ForeignKey('pages.id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('role', sa.String(32), server_default='editor')
    )

def downgrade():
    for t in [
        'memberships','notifications','integrations','sounds','focus_sessions','goals',
        'habits','events','task_subtasks','tasks','database_items','databases','pages','users']:
        op.drop_table(t)
